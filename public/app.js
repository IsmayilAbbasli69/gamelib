const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x020204, 0.05);

const camera = new THREE.PerspectiveCamera(40, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 0, 13);

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.outputEncoding = THREE.sRGBEncoding;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.body.appendChild(renderer.domElement);

const textureLoader = new THREE.TextureLoader();
textureLoader.crossOrigin = 'anonymous';

scene.add(new THREE.AmbientLight(0xffffff, 0.1));

const dirLight = new THREE.DirectionalLight(0x7da2ff, 0.8);
dirLight.position.set(-10, 8, 8);
dirLight.castShadow = true;
scene.add(dirLight);

const spotLight = new THREE.SpotLight(0xfff3e3, 3.0, 30, Math.PI / 4, 0.5, 1);
spotLight.position.set(0, 4, 8);
spotLight.castShadow = true;
scene.add(spotLight);
scene.add(spotLight.target);

const colors = {
    main: { spot: new THREE.Color(0xfff3e3), dir: new THREE.Color(0x7da2ff) }, 
    recs: { spot: new THREE.Color(0x00ffff), dir: new THREE.Color(0xff00ff) }, 
    favs: { spot: new THREE.Color(0xffd700), dir: new THREE.Color(0xff4500) }  
};
let targetSpotColor = new THREE.Color(colors.main.spot);
let targetDirColor = new THREE.Color(colors.main.dir);

const loadTex = (diff, bump, repX, repY) => {
    const col = textureLoader.load(diff);
    const bmp = textureLoader.load(bump);
    [col, bmp].forEach(t => { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(repX, repY); });
    return { map: col, bumpMap: bmp };
};

const wallMats = loadTex('https://threejs.org/examples/textures/brick_diffuse.jpg', 'https://threejs.org/examples/textures/brick_bump.jpg', 18, 4);
const advancedWallMat = new THREE.MeshStandardMaterial({ ...wallMats, bumpScale: 0.1, roughness: 0.8 });

const woodMats = loadTex('https://threejs.org/examples/textures/hardwood2_diffuse.jpg', 'https://threejs.org/examples/textures/hardwood2_bump.jpg', 8, 1);
const advancedWoodMat = new THREE.MeshStandardMaterial({ ...woodMats, bumpScale: 0.04, roughness: 0.6, metalness: 0.1 });

const plasticCaseMat = new THREE.MeshStandardMaterial({ color: 0x111113, roughness: 0.5, metalness: 0.1 });
const caseGeo = new THREE.BoxGeometry(1.6, 2.4, 0.25);

const worldGroup = new THREE.Group();
scene.add(worldGroup);

const frontWall = new THREE.Mesh(new THREE.PlaneGeometry(150, 50), advancedWallMat);
frontWall.position.set(0, -5, -3.5);
frontWall.receiveShadow = true;
worldGroup.add(frontWall);

// =========================================================================
// --- ULTRA REALİST: KENAR LEDLƏR, SPOT İŞIQLAR VƏ MƏRKƏZLƏŞMİŞ YAZI ---
// =========================================================================
const frameGroup = new THREE.Group();
frameGroup.position.set(-6, 3, -3.35); 
worldGroup.add(frameGroup);

// 1. Qalın Qara Taxta Kənar
const borderGeo = new THREE.BoxGeometry(2.2, 2.6, 0.1);
const borderMat = new THREE.MeshStandardMaterial({ color: 0x141414, roughness: 0.7 });
const frameBorder = new THREE.Mesh(borderGeo, borderMat);
frameBorder.castShadow = true;
frameGroup.add(frameBorder);

// 2. Krem Rəngli İç Kağız
const passepartoutGeo = new THREE.BoxGeometry(1.9, 2.3, 0.04);
const passepartoutMat = new THREE.MeshStandardMaterial({ color: 0xe8e4d9, roughness: 0.9 });
const frameInner = new THREE.Mesh(passepartoutGeo, passepartoutMat);
frameInner.position.z = 0.04;
frameGroup.add(frameInner);

// 3. Oyunçu Şəkli
const avatarGeo = new THREE.PlaneGeometry(1.5, 1.5);
let defaultAvatarTex = textureLoader.load("https://avatars.steamstatic.com/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb_full.jpg");
let avatarMat = new THREE.MeshStandardMaterial({ map: defaultAvatarTex, roughness: 0.2 });
const avatarMesh = new THREE.Mesh(avatarGeo, avatarMat);
avatarMesh.position.set(0, 0.25, 0.06);
frameGroup.add(avatarMesh);

// [YENİ] ŞƏKLİN ƏTRAFINDA DÖVR EDƏN İNCƏ LED XƏTLƏR (Neon Effekti)
const ledStripMat = new THREE.MeshStandardMaterial({ 
    color: 0xffffff, emissive: 0xfff3e3, emissiveIntensity: 1.5 
});
// Sol, Sağ, Üst və Alt kənar xətləri
const leftLed = new THREE.Mesh(new THREE.BoxGeometry(0.015, 1.52, 0.015), ledStripMat);
leftLed.position.set(-0.76, 0.25, 0.07);
const rightLed = new THREE.Mesh(new THREE.BoxGeometry(0.015, 1.52, 0.015), ledStripMat);
rightLed.position.set(0.76, 0.25, 0.07);
const topLed = new THREE.Mesh(new THREE.BoxGeometry(1.535, 0.015, 0.015), ledStripMat);
topLed.position.set(0, 1.01, 0.07);
const bottomLed = new THREE.Mesh(new THREE.BoxGeometry(1.535, 0.015, 0.015), ledStripMat);
bottomLed.position.set(0, -0.51, 0.07);
frameGroup.add(leftLed, rightLed, topLed, bottomLed);

// [YENİ] ŞƏKLƏ VURAN REAL SPOT İŞIQLAR (Yuxarı künclərdən şəklə fokuslanır)
const spotLeft = new THREE.SpotLight(0xfff3e3, 2.5, 4, Math.PI / 5, 0.6, 2);
spotLeft.position.set(-0.6, 1.1, 0.4);
spotLeft.target.position.set(0, 0.1, 0.06); // Şəklin mərkəzinə vurur
frameGroup.add(spotLeft);
frameGroup.add(spotLeft.target);

const spotRight = new THREE.SpotLight(0xfff3e3, 2.5, 4, Math.PI / 5, 0.6, 2);
spotRight.position.set(0.6, 1.1, 0.4);
spotRight.target.position.set(0, 0.1, 0.06);
frameGroup.add(spotRight);
frameGroup.add(spotRight.target);

// 4. Ad Canvas-ı (Yazı sahəsi)
const textCanvas = document.createElement('canvas');
textCanvas.width = 512;
textCanvas.height = 128;
const textCtx = textCanvas.getContext('2d');

const textTexture = new THREE.CanvasTexture(textCanvas);
const textGeo = new THREE.PlaneGeometry(1.6, 0.4);
const textMat = new THREE.MeshStandardMaterial({ map: textTexture, transparent: true, roughness: 0.5 });
const textMesh = new THREE.Mesh(textGeo, textMat);
textMesh.position.set(0, -0.75, 0.06); 
frameGroup.add(textMesh);

// 3D STATUS DİODU (Daha balanslı mərkəzə doğru sürüşdürüldü)
const statusSphereGeo = new THREE.SphereGeometry(0.035, 16, 16);
const statusSphereMat = new THREE.MeshStandardMaterial({ 
    color: 0x444444, emissive: 0x000000, emissiveIntensity: 0, roughness: 0.2
});
const statusSphereMesh = new THREE.Mesh(statusSphereGeo, statusSphereMat);
statusSphereMesh.position.set(-0.3, -0.75, 0.08); // X: -0.3 mükəmməl mərkəz balansı üçündür
frameGroup.add(statusSphereMesh);

let currentProfileName = "GİRİŞ GÖZLƏNİLİR";
let currentProfileStatus = false;

function drawPlayerInfo(name) {
    textCtx.clearRect(0, 0, 512, 128);
    
    // [YENİLƏNDİ] Yazı diodla birlikdə vizual olaraq tam mərkəzə oturacaq şəkildə nizamlandı
    textCtx.fillStyle = '#141414';
    textCtx.font = 'bold 36px Inter, sans-serif';
    textCtx.textBaseline = 'middle';
    textCtx.textAlign = 'left';
    
    let displayName = name.toUpperCase();
    if(displayName.length > 15) displayName = displayName.substring(0, 13) + "...";
    
    textCtx.fillText(displayName, 200, 64); // 200px koordinatı 3D diodla ahəngdar işləyir
    textTexture.needsUpdate = true;
}

drawPlayerInfo(currentProfileName);

// 5. Sənədli Şüşə Parıltısı (Spot işıqların şüşə üzərindəki parıltısı üçün)
const glassGeo = new THREE.PlaneGeometry(1.9, 2.3);
const glassMat = new THREE.MeshStandardMaterial({ 
    color: 0xffffff, transparent: true, opacity: 0.08, roughness: 0.02, metalness: 0.98 
});
const glassMesh = new THREE.Mesh(glassGeo, glassMat);
glassMesh.position.z = 0.07;
frameGroup.add(glassMesh);
// =========================================================================

const libraryGroup = new THREE.Group();
const favGroup = new THREE.Group();
const recGroup = new THREE.Group();

recGroup.position.set(-35, 0, 0);   
libraryGroup.position.set(0, 0, 0); 
favGroup.position.set(35, 0, 0);    
worldGroup.add(libraryGroup, favGroup, recGroup);

let targetCameraX = 0, targetGroupY = 0, inspectRotation = 0;
let selectedCassette = null, isScrollLocked = false, scrollTimeout = null;
let libraryCategories = [], activeCatIndex = 0;
let gameData = [];
const gameById = new Map();
const cassettes = [];

const viewState = {
    current: 'library',
    side: {
        favorites: { currentX: 0, maxScroll: 0, ids: [] },
        recommendations: { currentX: 0, maxScroll: 0, ids: [] },
    },
};

function createShelf(targetGroup, yPos) {
    const shelf = new THREE.Mesh(new THREE.BoxGeometry(32, 0.25, 2.5), advancedWoodMat);
    shelf.position.set(6, yPos - 1.4, -0.5);
    shelf.receiveShadow = true;
    shelf.castShadow = true;
    targetGroup.add(shelf);
}

function createCoverMaterial(coverUrl) {
    const coverTexture = textureLoader.load(coverUrl);
    coverTexture.encoding = THREE.sRGBEncoding;
    coverTexture.magFilter = THREE.LinearFilter;
    coverTexture.minFilter = THREE.LinearMipMapLinearFilter;
    coverTexture.generateMipmaps = true;
    return new THREE.MeshStandardMaterial({ map: coverTexture, roughness: 0.15, metalness: 0.1 });
}

function isCassetteVisibleInCurrentRoom(cassette) {
    if (viewState.current === 'library') {
        return cassette.userData.viewType === 'library' && cassette.userData.catIndex === activeCatIndex;
    }
    return cassette.userData.viewType === viewState.current;
}

function getViewHorizontalOffset(cassette) {
    if (cassette.userData.viewType === 'library') {
        return libraryCategories[cassette.userData.catIndex]?.currentX || 0;
    }
    return viewState.side[cassette.userData.viewType]?.currentX || 0;
}

function updateHud() {
    $('#category-hud').css('opacity', 0);
    clearTimeout(scrollTimeout);
    scrollTimeout = setTimeout(() => {
        if (viewState.current === 'library') {
            $('#category-hud').text(libraryCategories[activeCatIndex] ? libraryCategories[activeCatIndex].name : 'Kitabxana Boşdur');
        } else if (viewState.current === 'favorites') {
            $('#category-hud').text('Seçilmiş Oyunlar');
        } else {
            $('#category-hud').text('Xüsusi Tövsiyələr');
        }
        $('#category-hud').css('opacity', 1);
    }, 180);
}

function updateArrowVisibility() {
    let state = viewState.current === 'library' ? libraryCategories[activeCatIndex] : viewState.side[viewState.current];
    if (!state || state.maxScroll <= 0) {
        $('#arrow-left, #arrow-right').addClass('hidden');
        return;
    }
    $('#arrow-left').toggleClass('hidden', state.currentX >= 0);
    $('#arrow-right').toggleClass('hidden', state.currentX <= -state.maxScroll * 2.6);
}

function closeInspectPanel() {
    $('#info-panel').removeClass('active');
    $('#steam-login-box, #instructions').fadeIn(400);

    if (!selectedCassette) return;
    selectedCassette.userData.isAnimatingOut = false;
    setTimeout(() => {
        if (selectedCassette) selectedCassette.userData.parentGroup.attach(selectedCassette);
        selectedCassette = null;
        updateArrowVisibility();
    }, 600);
}

window.rotateRoom = function(direction) {
    if (direction === 'left') {
        targetCameraX = -35; viewState.current = 'recommendations';
        targetSpotColor.copy(colors.recs.spot); targetDirColor.copy(colors.recs.dir);
    } else if (direction === 'right') {
        targetCameraX = 35; viewState.current = 'favorites';
        targetSpotColor.copy(colors.favs.spot); targetDirColor.copy(colors.favs.dir);
    } else {
        targetCameraX = 0; viewState.current = 'library';
        targetSpotColor.copy(colors.main.spot); targetDirColor.copy(colors.main.dir);
    }
    closeInspectPanel(); updateHud(); updateArrowVisibility();
};

function addCassetteToScene(game, parentGroup, yPos, itemIndex, viewType, catIndex = -1) {
    const glossyFrontMat = createCoverMaterial(game.coverUrl);
    const materials = [plasticCaseMat, plasticCaseMat, plasticCaseMat, plasticCaseMat, glossyFrontMat, plasticCaseMat];
    const mesh = new THREE.Mesh(caseGeo, materials);

    mesh.position.set(-2.6 + itemIndex * 2.6, yPos, 0);
    mesh.castShadow = true; mesh.receiveShadow = true;

    mesh.userData = {
        id: game.id, title: game.title, tags: game.tags, desc: game.desc,
        viewType, catIndex, originalPos: mesh.position.clone(), originalRot: mesh.rotation.clone(),
        isAnimatingOut: false, parentGroup,
    };

    parentGroup.add(mesh);
    cassettes.push(mesh);
    return mesh;
}

function buildLibraryWall(data) {
    libraryCategories = data.categories.map((c) => {
        const gamesInCat = data.games.filter((g) => g.categoryId === c.id).length;
        return { ...c, currentX: 0, maxScroll: Math.max(gamesInCat - 4, 0) };
    });

    libraryCategories.forEach((cat) => createShelf(libraryGroup, cat.yPos));

    data.games.forEach((game) => {
        const catIndex = libraryCategories.findIndex((c) => c.id === game.categoryId);
        if (catIndex === -1) return;
        const rowGames = data.games.filter((g) => g.categoryId === game.categoryId);
        const itemIndex = rowGames.findIndex((g) => g.id === game.id);
        addCassetteToScene(game, libraryGroup, libraryCategories[catIndex].yPos, itemIndex, 'library', catIndex);
    });
}

function buildSideWall(sideName, shelfDict) {
    const sideGroup = sideName === 'favorites' ? favGroup : recGroup;
    const state = viewState.side[sideName];
    let maxLen = 0; let yOffset = 0; state.ids = [];

    Object.entries(shelfDict).forEach(([shelfName, ids]) => {
        const sideGames = ids.map(id => gameById.get(String(id))).filter(Boolean);
        if(sideGames.length > maxLen) maxLen = sideGames.length;
        createShelf(sideGroup, yOffset);
        sideGames.forEach((game, idx) => {
            state.ids.push(game.id);
            addCassetteToScene(game, sideGroup, yOffset, idx, sideName, -1);
        });
        yOffset -= 6;
    });
    state.currentX = 0; state.maxScroll = Math.max(maxLen - 4, 0);
}

function buildFromData(data) {
    gameData = data.games.slice();
    gameData.forEach((g) => gameById.set(String(g.id), g));

    buildLibraryWall(data);
    buildSideWall('favorites', data.shelves.favorites || {});
    buildSideWall('recommendations', data.shelves.recommendations || {});

    if (data.userProfile) {
        if (data.userProfile.avatar) {
            textureLoader.load(data.userProfile.avatar, (texture) => {
                texture.encoding = THREE.sRGBEncoding;
                avatarMesh.material.map = texture;
                avatarMesh.material.needsUpdate = true;
            });
        }
        const hasGames = data.games && data.games.length > 0;
        
        currentProfileName = data.userProfile.name;
        currentProfileStatus = hasGames;
        drawPlayerInfo(currentProfileName);
    }

    updateHud(); updateArrowVisibility();
}

function clearScene() {
    cassettes.forEach(c => {
        if(c.parent) c.parent.remove(c);
        c.geometry.dispose();
        if(Array.isArray(c.material)) c.material.forEach(m => m.dispose());
        else c.material.dispose();
    });
    cassettes.length = 0; gameById.clear();

    const cleanGroup = (group) => {
        while(group.children.length > 0) {
            const obj = group.children[0]; group.remove(obj);
            if(obj.geometry) obj.geometry.dispose();
            if(obj.material) obj.material.dispose();
        }
    };
    cleanGroup(libraryGroup); cleanGroup(favGroup); cleanGroup(recGroup);
    activeCatIndex = 0; targetGroupY = 0;
}

function loadSteamLibrary(steamId) {
    if (!steamId) return alert("Zəhmət olmasa düzgün Steam ID yazın!");
    $('#category-hud').text("YÜKLƏNİR...");
    
    fetch(`/api/steam/${steamId}`)
        .then((res) => {
            if (!res.ok) throw new Error('Profil gizlidir və ya server xətası baş verdi.');
            return res.json();
        })
        .then((data) => {
            if (data.games.length === 0) { alert("Oyun tapılmadı."); return; }
            clearScene();
            buildFromData(data);
        })
        .catch((err) => { alert(err.message); clearScene(); });
}

$('#steam-load-btn').on('click', () => {
    let inputVal = $('#steam-id-input').val().trim();
    const profileMatch = inputVal.match(/(?:profiles|id)\/([^\/\s]+)/);
    loadSteamLibrary(profileMatch ? profileMatch[1] : inputVal);
});

const fallbackData = {
    categories: [{ id: 'cat-pro', name: 'Məlumat gözlənilir...', yPos: 0 }],
    games: [], shelves: { favorites: {}, recommendations: {} }
};
buildFromData(fallbackData);

window.addEventListener('wheel', (e) => {
    if (selectedCassette || isScrollLocked) return;
    if (viewState.current === 'library') {
        if (e.deltaY > 0 && activeCatIndex < libraryCategories.length - 1) {
            isScrollLocked = true; activeCatIndex++; targetGroupY = -libraryCategories[activeCatIndex].yPos;
            updateHud(); updateArrowVisibility(); setTimeout(() => isScrollLocked = false, 500);
        } else if (e.deltaY < 0 && activeCatIndex > 0) {
            isScrollLocked = true; activeCatIndex--; targetGroupY = -libraryCategories[activeCatIndex].yPos;
            updateHud(); updateArrowVisibility(); setTimeout(() => isScrollLocked = false, 500);
        }
        return;
    }
    handleHorizontalScroll(e.deltaY > 0 ? 'right' : 'left');
});

$('#arrow-left').on('click', () => handleHorizontalScroll('left'));
$('#arrow-right').on('click', () => handleHorizontalScroll('right'));

function handleHorizontalScroll(direction) {
    if (selectedCassette) return;
    const step = 2.6 * 2;
    let state = viewState.current === 'library' ? libraryCategories[activeCatIndex] : viewState.side[viewState.current];
    if (!state) return;
    if (direction === 'right' && state.currentX > -state.maxScroll * 2.6) state.currentX -= step;
    else if (direction === 'left' && state.currentX < 0) state.currentX += step;
    updateArrowVisibility();
}

window.addEventListener('click', (event) => {
    if (selectedCassette || isScrollLocked || $(event.target).hasClass('nav-arrow') || $(event.target).is('button, input')) return;

    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);

    const intersects = raycaster.intersectObjects(cassettes);
    if (intersects.length === 0) return;

    const clickedObject = intersects[0].object;
    if (!isCassetteVisibleInCurrentRoom(clickedObject)) return;

    selectedCassette = clickedObject;
    scene.attach(selectedCassette);
    selectedCassette.userData.isAnimatingOut = true; inspectRotation = 0;

    $('#game-title').text(selectedCassette.userData.title);
    $('#game-desc').text(selectedCassette.userData.desc);
    $('#game-tags').html(selectedCassette.userData.tags.map(tag => `<span class="tag">${tag}</span>`).join(''));
    $('#panel-banner').attr('src', `https://steamcdn-a.akamaihd.net/steam/apps/${selectedCassette.userData.id}/header.jpg`);

    $('#info-panel').addClass('active');
    $('#steam-login-box, #instructions').fadeOut(300);
    $('.nav-arrow').addClass('hidden'); 
});

$('#close-btn').on('click', closeInspectPanel);

const mouse = new THREE.Vector2();
const raycaster = new THREE.Raycaster();
const clock = new THREE.Clock();

function animate() {
    requestAnimationFrame(animate);

    const elapsedTime = clock.getElapsedTime();
    const pulse = (Math.sin(elapsedTime * 3.8) + 1) / 2; 

    // Diod Status Animasiyası
    if (currentProfileStatus) {
        statusSphereMesh.material.color.setHex(0x27ae60);
        statusSphereMesh.material.emissive.setHex(0x27ae60);
        statusSphereMesh.material.emissiveIntensity = 1.0 + pulse * 3.0; 
    } else {
        statusSphereMesh.material.color.setHex(0x444444);
        statusSphereMesh.material.emissive.setHex(0x000000);
        statusSphereMesh.material.emissiveIntensity = 0;
    }

    const diffX = targetCameraX - camera.position.x;
    camera.position.x += diffX * 0.05;

    const swingAngle = diffX * -0.004; 
    camera.rotation.y = swingAngle; 
    camera.position.z = 13 + Math.abs(diffX) * 0.05;

    spotLight.position.x = camera.position.x;
    spotLight.target.position.x = camera.position.x; 
    dirLight.position.x = camera.position.x - 10;
    
    spotLight.color.lerp(targetSpotColor, 0.05);
    dirLight.color.lerp(targetDirColor, 0.05);

    libraryGroup.position.y += (targetGroupY - libraryGroup.position.y) * 0.08;

    cassettes.forEach((cassette) => {
        if (cassette === selectedCassette && cassette.userData.isAnimatingOut) {
            const targetPos = new THREE.Vector3(camera.position.x - 1.2, camera.position.y - 0.3, camera.position.z - 7.5);
            cassette.position.lerp(targetPos, 0.07);
            inspectRotation += 0.008;
            let targetRotY = 0.4 + swingAngle + Math.sin(inspectRotation) * 0.3;
            let targetRotX = 0.1 + Math.cos(inspectRotation) * 0.1;
            cassette.rotation.y += (targetRotY - cassette.rotation.y) * 0.07;
            cassette.rotation.x += (targetRotX - cassette.rotation.x) * 0.07;
            return;
        }

        const offsetX = getViewHorizontalOffset(cassette);
        if (cassette.parent === cassette.userData.parentGroup) {
            cassette.position.x += (cassette.userData.originalPos.x + offsetX - cassette.position.x) * 0.07;
            cassette.position.y += (cassette.userData.originalPos.y - cassette.position.y) * 0.07;
            cassette.position.z += (cassette.userData.originalPos.z - cassette.position.z) * 0.07;
        } else {
            const worldTarget = cassette.userData.originalPos.clone();
            worldTarget.x += offsetX + cassette.userData.parentGroup.position.x;
            worldTarget.y += cassette.userData.parentGroup.position.y;
            worldTarget.z += cassette.userData.parentGroup.position.z;
            cassette.position.lerp(worldTarget, 0.07);
        }
        cassette.rotation.y += (cassette.userData.originalRot.y - cassette.rotation.y) * 0.06;
        cassette.rotation.x += (cassette.userData.originalRot.x - cassette.rotation.x) * 0.06;
    });

    renderer.render(scene, camera);
}
animate();

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});