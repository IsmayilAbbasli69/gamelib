const express = require('express');
const path = require('path');
const app = express();

// "public" qovluğundakı index.html, styles.css və app.js-i brauzerə açırıq
app.use(express.static(path.join(__dirname, 'public')));

// Əsas səhifəyə girəndə index.html yüklənsin
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Port təyini (Deploy platformaları üçün process.env.PORT vacibdir)
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`🎮 3D Layihə aktivdir: http://localhost:${PORT}`);
});