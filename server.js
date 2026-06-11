const express = require('express');
const path = require('path');
const cors = require('cors');
const app = express();

app.use(cors());

// Qovluq yolunu tam təhlükəsiz və mütləq şəkildə təyin edirik
const publicPath = path.resolve(__dirname, 'public');

// Statik faylları qoşuruq
app.use(express.static(publicPath));

// Əsas səhifəyə istək gələndə index.html-i göndəririk
app.get('/', (req, res) => {
    res.sendFile(path.join(publicPath, 'index.html'));
});

// Port təyini
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`🎮 Server running on port ${PORT}`);
});