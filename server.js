require('dotenv').config();
const express = require('express');
const path = require('path');
const cors = require('cors');
const axios = require('axios');
const fs = require('fs');

const app = express();
app.use(cors());
app.use(express.json());

const publicPath = path.join(__dirname, 'public');
app.use(express.static(publicPath));

const STEAM_API_KEY = process.env.STEAM_API_KEY;

app.get('/api/steam/:steamId', async (req, requireRes) => {
    const { steamId } = req.params;

    if (!STEAM_API_KEY) {
        return requireRes.status(500).json({ error: "Serverdə STEAM_API_KEY təyin olunmayıb!" });
    }

    try {
        // 1. Oyunçunun Profil məlumatlarını (Şəkil və Ad) çəkmək
        const userUrl = `http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=${STEAM_API_KEY}&steamids=${steamId}`;
        const userResponse = await axios.get(userUrl);
        const playerData = userResponse.data.response.players[0] || null;

        let userProfile = {
            name: "GİRİŞ GÖZLƏNİLİR",
            avatar: "https://avatars.steamstatic.com/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb_full.jpg"
        };

        if (playerData) {
            userProfile.name = playerData.personaname;
            userProfile.avatar = playerData.avatarfull;
        }

        // 2. Oyunların siyahısını çəkmək
        const url = `http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=${STEAM_API_KEY}&steamid=${steamId}&include_appinfo=true&format=json`;
        const response = await axios.get(url);
        const steamGames = response.data.response.games || [];

        let games = steamGames.map(game => {
            const hoursPlayed = Math.round(game.playtime_forever / 60);
            let catId = 'cat-zero';
            if (hoursPlayed >= 100) catId = 'cat-pro';
            else if (hoursPlayed >= 10) catId = 'cat-mid';
            else if (hoursPlayed > 0) catId = 'cat-low';

            return {
                id: String(game.appid),
                title: game.name,
                categoryId: catId,
                hoursPlayed: hoursPlayed,
                tags: [hoursPlayed > 0 ? `${hoursPlayed} saat` : 'Oynanılmayıb'],
                desc: `Steam App ID: ${game.appid}. Toplam oynanılma müddəti: ${hoursPlayed} saat.`,
                coverUrl: `https://steamcdn-a.akamaihd.net/steam/apps/${game.appid}/library_600x900_2x.jpg`
            };
        });

        games.sort((a, b) => b.hoursPlayed - a.hoursPlayed);

        const baseCategories = [
            { id: 'cat-pro', name: 'Şah Əsərlər (100+ Saat)' },
            { id: 'cat-mid', name: 'Mütəmadi Oynanılan (10-100 Saat)' },
            { id: 'cat-low', name: 'Təsadüfi Oyun (1-10 Saat)' },
            { id: 'cat-zero', name: 'Gözləmədə Olanlar' }
        ];

        const activeCategories = baseCategories.filter(cat => games.some(g => g.categoryId === cat.id));
        const categories = activeCategories.map((cat, index) => ({ ...cat, yPos: index * -6 }));

        const ownedGameIds = new Set(games.map(g => g.id));
        const dbPath = path.join(__dirname, 'db.json');
        let fakeDB = [];
        if (fs.existsSync(dbPath)) fakeDB = JSON.parse(fs.readFileSync(dbPath, 'utf-8'));

        const availableRecs = fakeDB.filter(game => !ownedGameIds.has(game.id));
        const shuffledRecs = availableRecs.sort(() => 0.5 - Math.random()).slice(0, 10);
        const recTopShelf = []; const recBottomShelf = [];
        
        shuffledRecs.forEach((rec, idx) => {
            if(idx < 5) recTopShelf.push(rec.id);
            else recBottomShelf.push(rec.id);
            games.push({
                id: rec.id, title: rec.title, categoryId: 'hidden-recs', tags: rec.tags, desc: rec.desc,
                coverUrl: `https://steamcdn-a.akamaihd.net/steam/apps/${rec.id}/library_600x900_2x.jpg`
            });
        });

        const myGameIds = games.filter(g => g.categoryId !== 'hidden-recs').map(g => g.id); 
        const shelves = {
            favorites: { "⭐ Seçilmiş Oyunlar": myGameIds.slice(0, 5) },
            recommendations: { "🔥 İsti Tövsiyələr": recTopShelf, "🎯 Fərqli Tərzlər": recBottomShelf }
        };

        requireRes.json({ userProfile, categories, games, shelves });

    } catch (error) {
        console.error("Steam API Error:", error.message);
        requireRes.status(500).json({ error: "Steam məlumatları gətirilə bilmədi." });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`🎮 Server ${PORT} portunda aktivdir.`));