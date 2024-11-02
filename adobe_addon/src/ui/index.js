import addOnUISdk from "https://cdn.adobe.io/adobe-express-addon/latest/express-addon.js";

addOnUISdk.ready.then(() => {
    initializeAddon();
});

async function initializeAddon() {
    document.getElementById('applyBrassEffect').addEventListener('click',applyBrassEffect);
    document.getElementById('addGears').addEventListener('click', addGearElements);
    document.getElementById('generateSteam').addEventListener('click',generateSteamEffect);

    await initializeTools();
}

async function applyBrassEffect() {
    try {
        const selection = await addOnUISdk.app.document.getSelection();
        if (!selection.items.length){
            throw new Error('No elements selected.');
        }

        await addOnUISdk.app.document.addEditingControl({
            type: 'filter',
            settings: {
                brightness: 1.2,
                contrast: 1.1,
                saturation: 0.9,
                temperature: 40,
                tint: 10
            }
        });

        await addMetallicTexture(selection);

    } catch (error) {
        console.error('Error applying brass effect:', error);
        showErrorNotifications(error.message);
    }
    }

async function addGearElements() {
    try {

        const gearAssets = await loadGearAssets();
        

        const composition = await createGearComposition(gearAssets);

        await addOnUISdk.app.document.addElements([composition]);
       
    } catch (error) {
        console.error('Errer adding gears:', error);
        showErrorNotifications(error.message);
    }
}

async function generateSteamEffect() {
    try {
        const steamParticles = await createSteamParticles();
        
        await animateSteamParticles(steamParticles);

        await addOnUISdk.app.document.addElements([steamParticles]);
    } catch (error) {
        console.error('Error generating steam:', error);
        showErrorNotifications(error.message);
    }
}

async function createGearComposition(assets) {
    return new Promise(async (resolve) => {
        const composition = {
            type: 'group',
            items: []
        };

        for (const gear of assets) {
            const gearElement = {
                type: 'image',
                src: gear.url,
                transform: {
                    rotation: Math.random() * 360,
                    scale: 0.5 + Math.random() * 1
                }
            };
            composition.items.push(gearElement);
        }

        resolve(composition);
    });
}

async function createSteamParticles() {
    return {
        type: 'effect',
        effect: 'particle',
        settings: {
            particleCount: 100,
            particleSize: {min: 2, max: 8},
            opacity: {start: 0.8, end: 0},
            velocity: {min: 1, max: 3},
            direction: 90,
            spread: 30,
            lifetime: {min: 1, max: 3},
            emissionRate: 20
        }
    };
}

class SteampunkAssetManager {
    constructor() {
        this.categories = {
            gears: [],
            pipes: [],
            dials: [],
            textures: []
        }
    }

    async initialize() {
        await this.loadAssets();
        await this.registerCustomControls();
    }

    async loadAssets() {
        const assetManifeset = await fetch();
        const assets = await assetManifest.json();

        for (const asset of assets) {
            if (this.categories[asset.category]) {
                this.categories[asset.category].push(asset);
            }
        }
    }

    async registerCustomControls() {
        for (const category in this.categories) {
            await addOnUISdk.app.document.registerCustomControl({
                id: `steampunk-${category}`,
                label: `Steampunk ${category.charAt(0).toUpperCase() + category.slice(1)}`,
                items: this.categories[category]
            });
        }
    }
}

class SteampunkEffectsSystem {
    constructor() {
        this.effects = new Map();
    }

    registerEffect(name, effect){
        this.effects.set(name, effect);
    }

    async applyEffect(name, element){
        const effect = this.effects.get(name);
        if (!effect) {
            throw new Error(`Effect '${name} not found`);
        }

        return await effect(element);
    }
}

const effectSystem = new SteampunkEffectsSystem();

effectSystem.registerEffect('brass', async (element) => {
    const brassEffect = {
        type: 'material',
        settings: {
            metallic: 0.8,
            roughness: 0.3,
            color: '#b5a642',
            normalMap: 'brass-normal.jpg',
            ambientOcclusion: 'brass-ao.jpg'
        }
    };

    return await addOnUISdk.app.document.applyEffect(element, brassEffect);
});

effectSystem.registerEffect('copper', async (element) => {
    const copperEffect = {
        type: 'material',
        settings: {
            metallic: 0.9,
            roughness: 0.2,
            color: '#b87333',
            normalMap: 'copper-normal.jpg',
            ambientOcclusion: 'copper-ao.jpg'
        }
    };

    return await addOnUISdk.app.document.applyEffect(element,copperEffect);
});

