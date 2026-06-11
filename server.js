const express = require('express');
const path = require('path');
const cors = require('cors');
const app = express();

app.use(cors());

// Mütləq və dəqiq qovluq yolu
const publicPath = path.join(__dirname, 'public');

// 1. Statik faylların oxunması üçün əsas ayar
app.use(express.static(publicPath));

// 2. Əsas səhifə root marşrutu
app.get('/', (req, res) => {
    res.sendFile(path.join(publicPath, 'index.html'));
});

// 3. FİX: Səhifə yenilənəndə (Refresh) "Not Found" xətası olmasın deyə bura yönləndiririk
app.get('*', (req, res) => {
    res.sendFile(path.join(publicPath, 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`🎮 Server running perfectly on port ${PORT}`);
});