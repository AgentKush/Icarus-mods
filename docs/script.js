/* ═══════════════════════════════════════════
   AgentKush Icarus Mods — script.js
   Particle canvas (credit: Zayon) + catalog
   + Premium effects: scramble, tilt, magnetic,
     spotlight, card glow
   ═══════════════════════════════════════════ */

// --- PARTICLE CANVAS (Zayon's moving dots) ---
// OffscreenCanvas when supported (separate thread), fallback to main thread
const canvas = document.getElementById('particle-canvas');
const rootStyles = getComputedStyle(document.documentElement);
const accentMatch = rootStyles.getPropertyValue('--accent-rgb').trim();
const rgbAccent = accentMatch || '232, 123, 53';

let particleWorker = null;

if (canvas.transferControlToOffscreen && window.Worker) {
    // --- OFFSCREEN PATH: particles run on a Web Worker ---
    try {
        const offscreen = canvas.transferControlToOffscreen();
        particleWorker = new Worker('./particle-worker.js');
        particleWorker.postMessage({
            type: 'init',
            canvas: offscreen,
            width: window.innerWidth,
            height: window.innerHeight,
            accent: rgbAccent
        }, [offscreen]);

        window.addEventListener('resize', () => {
            particleWorker.postMessage({
                type: 'resize',
                width: window.innerWidth,
                height: window.innerHeight
            });
        });
    } catch (e) {
        // OffscreenCanvas transfer failed, fall through to main thread
        particleWorker = null;
    }
}

if (!particleWorker) {
    // --- MAIN THREAD FALLBACK ---
    const ctx = canvas.getContext('2d');
    let width, height, particles;

    function initParticles() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
        particles = [];
        const count = Math.min(120, Math.floor(width * height / 8000));
        for (let i = 0; i < count; i++) {
            particles.push({
                x: Math.random() * width,
                y: Math.random() * height,
                radius: Math.random() * 2 + 0.5,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                opacity: Math.random() * 0.5 + 0.1
            });
        }
    }

    function animateParticles() {
        ctx.clearRect(0, 0, width, height);
        particles.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;
            if (p.x < 0) p.x = width;
            if (p.x > width) p.x = 0;
            if (p.y < 0) p.y = height;
            if (p.y > height) p.y = 0;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(${rgbAccent}, ${p.opacity})`;
            ctx.shadowBlur = 10;
            ctx.shadowColor = `rgba(${rgbAccent}, 0.6)`;
            ctx.fill();
        });
        requestAnimationFrame(animateParticles);
    }

    window.addEventListener('resize', initParticles);
    initParticles();
    animateParticles();
}

// --- MOD DATA ---
const MODS=[{"name": "Absolute Chaos - Core","folder": "AbsoluteChaos_Core","version": "0.2.1","description": "Base layer of the Absolute Chaos modpack.","category": "Mod Packs","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/AbsoluteChaos_Core","download": "https://github.com/AgentKush/Icarus-mods/raw/main/AbsoluteChaos_Core/AbsoluteChaos_Core.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/AbsoluteChaos_Core-v0.2.1","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/AbsoluteChaos_Core/Banner.png"},{"name": "Agent's BioLab","folder": "Agents_BioLab","version": "2.0","description": "Adds all Bio Lab Legendary weapons to the Workshop! Includes Frontier Revolver, Kinetic Rifle, Tactical Bow, Mining Armature, Ape Club, Heavy Flamethrower, Anti-materiel Rifle, Javelin Launcher, Sl...","category": "Workshop & Items","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Agents_BioLab","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Agents_BioLab/Agents_BioLab.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Agents_BioLab-v2.0","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Agents_BioLab/Banner.png"},{"name": "Agents Individual Item Kits","folder": "Agents_Individual_Item_Kits","version": "5.2","description": "Ver 5.2\n\u2014 Fixed workshop grid: items no longer clip into the top sell bar (Y offset shifted from 100 to 250)\n\u2014 Re-sorted all 2,683 kits into 20 category groups with box-width spacing between each g...","category": "Workshop & Items","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Agents_Individual_Item_Kits","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Agents_Individual_Item_Kits/Agents_Individual_Item_Kits.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Agents_Individual_Item_Kits-v5.2","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Agents_Individual_Item_Kits/Banner.png"},{"name": "Always Show Buildings On Map","folder": "Always_show_buildings_on_map","version": "1.0","description": "Always shows player-built structures on the map and minimap without requiring any special stats or radar.","category": "Building & Construction","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Always_show_buildings_on_map","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Always_show_buildings_on_map/Always_show_buildings_on_map.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Always_show_buildings_on_map-v1.0","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Always_show_buildings_on_map/Banner.png"},{"name": "Ammo Crafting Overhaul","folder": "Ammo_Crafting_Overhaul","version": "1.2","description": "v1.2: Added 50x batch crafting for Sniper special ammo (Explosive, Incendiary) \u2014 previously missing. | 48 new ammo recipes.","category": "Combat & Defense","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Ammo_Crafting_Overhaul","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Ammo_Crafting_Overhaul/Ammo_Crafting_Overhaul.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Ammo_Crafting_Overhaul-v1.2","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Ammo_Crafting_Overhaul/Banner.png"},{"name": "Armor Attachment Expansion","folder": "Armor_Attachment_Expansion","version": "1.0","description": "v1.0: Adds 25 new craftable armor attachments (5 per body part: Head, Arms, Body, Legs, Feet). All use base-game stat keys so effects stack cleanly with existing talents, food buffs, and other atta...","category": "Uncategorized","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Armor_Attachment_Expansion","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Armor_Attachment_Expansion/Armor_Attachment_Expansion.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Armor_Attachment_Expansion-v1.0","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Armor_Attachment_Expansion/Banner.png"},{"name": "Armor Set Bonuses Enhanced","folder": "Armor_Set_Bonuses_Enhanced","version": "2.0","description": "Enhanced armor set bonuses with 3-piece partial bonuses for mix-and-match builds.","category": "Combat & Defense","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Armor_Set_Bonuses_Enhanced","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Armor_Set_Bonuses_Enhanced/Armor_Set_Bonuses_Enhanced.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Armor_Set_Bonuses_Enhanced-v2.0","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Armor_Set_Bonuses_Enhanced/Banner.png"},{"name": "Bestiary Fix","folder": "Bestiary_Fix","version": "1.1","description": "Adds missing Kill/Skin experience events for Sulfur Worm, Sulfur Vesper, Cave Worm, and Vesper to help Bestiary tracking.","category": "Quality of Life","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Bestiary_Fix","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Bestiary_Fix/Bestiary_Fix.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Bestiary_Fix-v1.1","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Bestiary_Fix/Banner.png"},{"name": "Better Mission Rewards","folder": "Better_Mission_Rewards","version": "1.0","description": "v1.0: Doubles mission payouts - 2x credits, 2x account XP, and 2x faction reputation across all faction missions. Less mission grinding, same gameplay flow. Talent unlocks are untouched.","category": "Uncategorized","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Better_Mission_Rewards","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Better_Mission_Rewards/Better_Mission_Rewards.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Better_Mission_Rewards-v1.0","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Better_Mission_Rewards/Banner.png"},{"name": "Creature Difficulty Scaling","folder": "Creature_Difficulty_Scaling","version": "2.3","description": "Dynamic creature level scaling for level 500 cap. v2.3: DarkAngel edition \u2014 adds affliction system (poison, concussion, sprains, bee swarms, komodo bites, sandworm poison, enraged buff), epic creat...","category": "Survival & Difficulty","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Creature_Difficulty_Scaling","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Creature_Difficulty_Scaling/Creature_Difficulty_Scaling.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Creature_Difficulty_Scaling-v2.3","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Creature_Difficulty_Scaling/Banner.png"},{"name": "Creature Drop Enhancer","folder": "Creature_Drop_Enhancer","version": "1.2","description": "v1.2: Extended doubled butchery/skinning drops to 15 more creatures (Komodo, Orka, Storca, Slinker, juveniles, tundra fauna). | Doubles all creature butchery and skinning outputs across 62 recipes.","category": "Survival & Difficulty","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Creature_Drop_Enhancer","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Creature_Drop_Enhancer/Creature_Drop_Enhancer.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Creature_Drop_Enhancer-v1.2","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Creature_Drop_Enhancer/Banner.png"},{"name": "Culinex Food Boost Fix","folder": "Culinex_Food_Boost_Fix","version": "2.9","description": "v2.9: Fixed remaining D_ItemsStatic reference in Raw_Chicken_Butchery input (crash fix for butcher bench). All recipe references now use D_ItemTemplate. | Fixes Culinex (Chef's Backpack) 25% food e...","category": "Food & Consumables","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Culinex_Food_Boost_Fix","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Culinex_Food_Boost_Fix/Culinex_Food_Boost_Fix.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Culinex_Food_Boost_Fix-v2.9","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Culinex_Food_Boost_Fix/Banner.png"},{"name": "Dev Tools Kit","folder": "Dev_Tools_Kit","version": "1.1.5","description": "v1.1.3: Substituted visible meshes for 3 tools that previously used the invisible placeholder (Inspection Tool \u2192 Scanner mesh, Bug Tool \u2192 Beacon mesh, Transform Tool \u2192 Building Hammer mesh); added ...","category": "Workshop & Items","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Dev_Tools_Kit","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Dev_Tools_Kit/Dev_Tools_Kit.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Dev_Tools_Kit-v1.1.5","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Dev_Tools_Kit/Banner.png"},{"name": "Exotic Economy Overhaul","folder": "Exotic_Economy_Overhaul","version": "2.1","description": "v2.1: Crash fix - all recipe outputs corrected from D_ItemsStatic to D_ItemTemplate. Added 14 missing buy/sell recipes (Refined Copper, Refined Metal, sell-back for all buyable materials). 66 total...","category": "Economy & Resources","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Exotic_Economy_Overhaul","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Exotic_Economy_Overhaul/Exotic_Economy_Overhaul.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Exotic_Economy_Overhaul-v2.1","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Exotic_Economy_Overhaul/Banner.png"},{"name": "Extended Deep Ore Scanner Range","folder": "Extended_Deep_Ore_Scanner_Range","version": "1.0","description": "10x detection range for the Deep Ore Scanner. Find deep exotic and epic ore deposits from 3000m (3km) instead of 300m.","category": "Uncategorized","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Extended_Deep_Ore_Scanner_Range","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Extended_Deep_Ore_Scanner_Range/Extended_Deep_Ore_Scanner_Range.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Extended_Deep_Ore_Scanner_Range-v1.0","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Extended_Deep_Ore_Scanner_Range/Banner.png"},{"name": "Extended Scanner Range","folder": "Extended_Scanner_Range","version": "1.0","description": "10x detection range for the Cave Scanner and Fish Finder - locate caves and fishing spots from far further out.","category": "Uncategorized","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Extended_Scanner_Range","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Extended_Scanner_Range/Extended_Scanner_Range.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Extended_Scanner_Range-v1.0","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Extended_Scanner_Range/Banner.png"},{"name": "Extended Spoil Timers","folder": "Extended_Spoil_Timers","version": "1.2","description": "Extends decay timers on 29 items.","category": "Food & Consumables","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Extended_Spoil_Timers","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Extended_Spoil_Timers/Extended_Spoil_Timers.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Extended_Spoil_Timers-v1.2","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Extended_Spoil_Timers/Banner.png"},{"name": "Extended Wire and Pipe Tool","folder": "Extended_Wire_and_Pipe_Tool","version": "1.0","description": "Extends power cable and water/fuel pipe connection range by 10x.","category": "Building & Construction","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Extended_Wire_and_Pipe_Tool","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Extended_Wire_and_Pipe_Tool/Extended_Wire_and_Pipe_Tool.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Extended_Wire_and_Pipe_Tool-v1.0","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Extended_Wire_and_Pipe_Tool/Banner.png"},{"name": "Fast Processing (10x)","folder": "FastProcessing_All_10x","version": "5.1","description": "v5.1: Fixed the Scoria brick roof corner recipe so it gets the speed boost (the game's recipe name is misspelled 'Scoria_Bick_Roof_Corner'). | All crafting and processing 10x faster.","category": "Processing Speed","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/FastProcessing_All_10x","download": "https://github.com/AgentKush/Icarus-mods/raw/main/FastProcessing_All_10x/FastProcessing_All_10x.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/FastProcessing_All_10x-v5.1","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/FastProcessing_All_10x/Banner.png"},{"name": "Fast Processing (15x)","folder": "FastProcessing_All_15x","version": "5.1","description": "v5.1: Fixed the Scoria brick roof corner recipe so it gets the speed boost (the game's recipe name is misspelled 'Scoria_Bick_Roof_Corner'). | All crafting and processing 15x faster.","category": "Processing Speed","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/FastProcessing_All_15x","download": "https://github.com/AgentKush/Icarus-mods/raw/main/FastProcessing_All_15x/FastProcessing_All_15x.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/FastProcessing_All_15x-v5.1","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/FastProcessing_All_15x/Banner.png"},{"name": "Fast Processing (25x)","folder": "FastProcessing_All_25x","version": "5.1","description": "v5.1: Fixed the Scoria brick roof corner recipe so it gets the speed boost (the game's recipe name is misspelled 'Scoria_Bick_Roof_Corner'). | All crafting and processing 25x faster.","category": "Processing Speed","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/FastProcessing_All_25x","download": "https://github.com/AgentKush/Icarus-mods/raw/main/FastProcessing_All_25x/FastProcessing_All_25x.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/FastProcessing_All_25x-v5.1","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/FastProcessing_All_25x/Banner.png"},{"name": "Fast Processing (5x)","folder": "FastProcessing_All_5x","version": "5.1","description": "v5.1: Fixed the Scoria brick roof corner recipe so it gets the speed boost (the game's recipe name is misspelled 'Scoria_Bick_Roof_Corner'). | All crafting and processing 5x faster.","category": "Processing Speed","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/FastProcessing_All_5x","download": "https://github.com/AgentKush/Icarus-mods/raw/main/FastProcessing_All_5x/FastProcessing_All_5x.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/FastProcessing_All_5x-v5.1","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/FastProcessing_All_5x/Banner.png"},{"name": "Fast Processing (Instant)","folder": "FastProcessing_Instant","version": "5.1","description": "v5.1: Fixed the Scoria brick roof corner recipe so it gets the speed boost (the game's recipe name is misspelled 'Scoria_Bick_Roof_Corner'). | All crafting and processing instant.","category": "Processing Speed","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/FastProcessing_Instant","download": "https://github.com/AgentKush/Icarus-mods/raw/main/FastProcessing_Instant/FastProcessing_Instant.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/FastProcessing_Instant-v5.1","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/FastProcessing_Instant/Banner.png"},{"name": "Faster Crafting","folder": "Faster_Crafting","version": "1.6","description": "v1.6: Fixed the Scoria brick roof corner recipe so it gets the speed boost (the game's recipe name is misspelled 'Scoria_Bick_Roof_Corner'). | All crafting and processing 2x faster.","category": "Processing Speed","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Faster_Crafting","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Faster_Crafting/Faster_Crafting.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Faster_Crafting-v1.6","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Faster_Crafting/Banner.png"},{"name": "Faster Harvest Tools","folder": "Faster_Harvest_Tools","version": "1.0","description": "2x harvest yield from every gathering tool - mining, felling, reaping and skinning - plus faster tree felling.","category": "Uncategorized","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Faster_Harvest_Tools","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Faster_Harvest_Tools/Faster_Harvest_Tools.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Faster_Harvest_Tools-v1.0","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Faster_Harvest_Tools/Banner.png"},{"name": "Fish and Farming Boost","folder": "Fish_Farming_Boost","version": "1.3","description": "v1.3: Added the 13 Elysium (ELY) fish spawn zones for full fishing coverage (70/70 zones), boosted to match the rest of the mod (2x spawn rate, 1.5x fish quality). | Farming and fishing overhaul.","category": "Food & Consumables","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Fish_Farming_Boost","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Fish_Farming_Boost/Fish_Farming_Boost.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Fish_Farming_Boost-v1.3","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Fish_Farming_Boost/Banner.png"},{"name": "Genetic Mastery","folder": "Genetic_Mastery","version": "1.0","description": "Elite trait lineages (Brave, Hardy, Bold, Careful and more) are 4x more common - wild and bred creatures far more often carry powerful genetics. Distinct from Genetics & Breeding Overhaul (mutation...","category": "Uncategorized","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Genetic_Mastery","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Genetic_Mastery/Genetic_Mastery.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Genetic_Mastery-v1.0","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Genetic_Mastery/Banner.png"},{"name": "Genetics & Breeding Overhaul","folder": "Genetics_Breeding_Overhaul","version": "1.0","description": "v1.0: Supercharges the Mendel genetics system - doubles genotype/phenotype mutation, twin-birth, gestation, recovery and lineage-mutation chances from the Genetics talents, and rebalances bloodline...","category": "Uncategorized","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Genetics_Breeding_Overhaul","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Genetics_Breeding_Overhaul/Genetics_Breeding_Overhaul.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Genetics_Breeding_Overhaul-v1.0","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Genetics_Breeding_Overhaul/Banner.png"},{"name": "Hardcore Rebalance Pack","folder": "Hardcore_Rebalance_Pack","version": "2.1","description": "v2.1: Removed 4 stale XP-event references (KillAI/KillSmallAnimal/KillMediumAnimal/Kill_RadiationBoss) that the game has since replaced with per-creature events. | For survivors who think Icarus is...","category": "Survival & Difficulty","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Hardcore_Rebalance_Pack","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Hardcore_Rebalance_Pack/Hardcore_Rebalance_Pack.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Hardcore_Rebalance_Pack-v2.1","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Hardcore_Rebalance_Pack/Banner.png"},{"name": "Hidden Building Pieces","folder": "Hidden_Building_Pieces","version": "4.4","description": "Unlocks hidden building pieces: Wood diagonal/curved, frames, corner stairs, glass stairs, and more.\n\nv4.1 \u2014 Added Interior Wood Floor recipe at Fabricator/Manufacturer (the forgotten floor)\nv4.0 \u2014...","category": "Building & Construction","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Hidden_Building_Pieces","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Hidden_Building_Pieces/Hidden_Building_Pieces.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Hidden_Building_Pieces-v4.4","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Hidden_Building_Pieces/Banner.png"},{"name": "Hunter's Critical Strike","folder": "Hunters_Critical_Strike","version": "1.0","description": "Weak-point hits deal far more critical damage - regular weak points now hit as hard as elite ones. Rewards precision aiming. First-ever crit-system mod.","category": "Uncategorized","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Hunters_Critical_Strike","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Hunters_Critical_Strike/Hunters_Critical_Strike.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Hunters_Critical_Strike-v1.0","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Hunters_Critical_Strike/Banner.png"},{"name": "Indestructible Tools & Weapons","folder": "Indestructible_Tools_Weapons","version": "1.9","description": "All tools, weapons, armor, buildings, doors, and crafting stations will never break.","category": "Quality of Life","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Indestructible_Tools_Weapons","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Indestructible_Tools_Weapons/Indestructible_Tools_Weapons.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Indestructible_Tools_Weapons-v1.9","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Indestructible_Tools_Weapons/Banner.png"},{"name": "Lightweight Hauling","folder": "Lightweight_Hauling","version": "1.0","description": "All ores, ingots and raw resources weigh 50% less - haul far more per trip.","category": "Uncategorized","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Lightweight_Hauling","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Lightweight_Hauling/Lightweight_Hauling.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Lightweight_Hauling-v1.0","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Lightweight_Hauling/Banner.png"},{"name": "Mining Laser Overclock","folder": "Mining_Laser_Overclock","version": "1.0","description": "No more overheating. The mining laser runs 300 seconds of continuous use before overheating (was 5s) and cools 5x faster. Sustained, uninterrupted deep mining. First-ever mining-laser blueprint mod.","category": "Uncategorized","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Mining_Laser_Overclock","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Mining_Laser_Overclock/Mining_Laser_Overclock.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Mining_Laser_Overclock-v1.0","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Mining_Laser_Overclock/Banner.png"},{"name": "Modular Affliction Adjuster","folder": "Modular_Affliction_Adjuster","version": "2.0","description": "Comprehensive affliction adjustment - reduces stat penalties by ~50%, extends escalation times by ~50%, and reduces damage over time by ~50%.","category": "Quality of Life","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Modular_Affliction_Adjuster","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Modular_Affliction_Adjuster/Modular_Affliction_Adjuster.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Modular_Affliction_Adjuster-v2.0","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Modular_Affliction_Adjuster/Banner.png"},{"name": "Modular Buff Enhancer","folder": "Modular_Buff_Enhancer","version": "1.1","description": "Comprehensive buff enhancement - 83 core buffs plus 156 food buffs, all boosted by ~50%.","category": "Quality of Life","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Modular_Buff_Enhancer","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Modular_Buff_Enhancer/Modular_Buff_Enhancer.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Modular_Buff_Enhancer-v1.1","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Modular_Buff_Enhancer/Banner.png"},{"name": "More Eye Colours","folder": "MoreEyeColours","version": "2.0","description": "Massive eye color expansion - 60 new colors across every color family, plus unlocked hidden content.","category": "Quality of Life","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/MoreEyeColours","download": "https://github.com/AgentKush/Icarus-mods/raw/main/MoreEyeColours/MoreEyeColours.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/MoreEyeColours-v2.0","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/MoreEyeColours/Banner.png"},{"name": "Night Vision Goggles","folder": "NightVisionGoggles","version": "2.1","description": "v2.1: Fixed 0 recipe outputs from D_ItemsStatic to D_ItemTemplate (crash fix). | Adds craftable Night Vision Goggles with improved durability, no decay, lighter weight.","category": "Workshop & Items","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/NightVisionGoggles","download": "https://github.com/AgentKush/Icarus-mods/raw/main/NightVisionGoggles/NightVisionGoggles.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/NightVisionGoggles-v2.1","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/NightVisionGoggles/Banner.png"},{"name": "No Food Spoilage","folder": "No_Food_Spoilage","version": "2.2","description": "v2.2: Restored coconut ripening (young -> mid -> mature) that the no-spoil change had broken; mature coconuts still never rot. | Prevents all food spoilage.","category": "Food & Consumables","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/No_Food_Spoilage","download": "https://github.com/AgentKush/Icarus-mods/raw/main/No_Food_Spoilage/No_Food_Spoilage.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/No_Food_Spoilage-v2.2","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/No_Food_Spoilage/Banner.png"},{"name": "Passive Ore Extractor Drills","folder": "Passive_Ore_Extractor_Drills","version": "7.7","description": "23 passive ore extractors - one per ore type.","category": "Economy & Resources","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Passive_Ore_Extractor_Drills","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Passive_Ore_Extractor_Drills/Passive_Ore_Extractor_Drills.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Passive_Ore_Extractor_Drills-v7.7","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Passive_Ore_Extractor_Drills/Banner.png"},{"name": "Performance Optimizer","folder": "Performance_Optimizer","version": "2.2","description": "Comprehensive FPS optimization - PAK config overrides (foliage/shadow/fog/LOD reduction) plus data table changes (reduced spawns, slower hordes, extended decay, boosted fuel, weather tuning).","category": "Quality of Life","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Performance_Optimizer","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Performance_Optimizer/Performance_Optimizer.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Performance_Optimizer-v2.2","banner": ""},{"name": "Resource Repacker","folder": "Resource_Repacker","version": "1.3","description": "v1.3: Removed the D_Itemable tooltip override that was breaking the DLC kit icons and display names (the EXMOD merge replaces full rows rather than patching fields). DLC requirement is now in the R...","category": "Uncategorized","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Resource_Repacker","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Resource_Repacker/Resource_Repacker.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Resource_Repacker-v1.3","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Resource_Repacker/Banner.png"},{"name": "Solar Panel Expansion","folder": "Solar_Panel_Expansion","version": "1.1","description": "v1.1: Added the Bunker Solar Panel as a 4th workshop kit. | Adds all solar panels and the solar backpack to a dedicated Workshop tab with fair pricing.","category": "Workshop & Items","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Solar_Panel_Expansion","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Solar_Panel_Expansion/Solar_Panel_Expansion.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Solar_Panel_Expansion-v1.1","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Solar_Panel_Expansion/Banner.png"},{"name": "Stack Size Overhaul","folder": "Stack_Size_Overhaul","version": "1.5","description": "v1.5: Removed a stale entry for a test item (Item_Light_Test) that no longer exists in the game. | Increases stack sizes on 1262 items.","category": "Economy & Resources","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Stack_Size_Overhaul","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Stack_Size_Overhaul/Stack_Size_Overhaul.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Stack_Size_Overhaul-v1.5","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Stack_Size_Overhaul/Banner.png"},{"name": "Survival Attachments","folder": "Survival_Attachments","version": "1.1","description": "v1.1: Added Arms (Endurance Brace, -25% stamina use) and Feet (Recovery Treads, +25% stamina regen) survival attachments to fill the previously-empty arms/feet slots. | Doubles armor attachment slo...","category": "Uncategorized","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Survival_Attachments","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Survival_Attachments/Survival_Attachments.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Survival_Attachments-v1.1","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Survival_Attachments/Banner.png"},{"name": "Taming & Tames Overhaul","folder": "Taming_Tames_Overhaul","version": "1.1","description": "v1.1: Added faster mounts (Husbandry_MountSpeed 5% -> 20%) and cheaper riding (Husbandry_RidingEfficiency doubled). | Faster taming (3x), faster breeding (2x), easier upkeep, faster tame growth acr...","category": "Uncategorized","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Taming_Tames_Overhaul","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Taming_Tames_Overhaul/Taming_Tames_Overhaul.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Taming_Tames_Overhaul-v1.1","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Taming_Tames_Overhaul/Banner.png"},{"name": "Tier Upgrade Forge","folder": "Tier_Upgrade_Forge","version": "1.3","description": "v1.3: Added in-place tier upgrades for Spears (Wood->Metal->Steel->Platinum->Titanium + Obsidian/ColdSteel/IronWood), Shovels (Stone->Platinum->Titanium), Sickles (Bone->Platinum->Titanium + specia...","category": "Economy & Resources","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Tier_Upgrade_Forge","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Tier_Upgrade_Forge/Tier_Upgrade_Forge.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Tier_Upgrade_Forge-v1.3","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Tier_Upgrade_Forge/Banner.png"},{"name": "Trap and Defense Expansion","folder": "Trap_Defense_Expansion","version": "1.2","description": "v1.2: Fixed 23 recipe outputs from D_ItemsStatic to D_ItemTemplate (crash fix). | Defense expansion with 23 recipes using real game items.","category": "Combat & Defense","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Trap_Defense_Expansion","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Trap_Defense_Expansion/Trap_Defense_Expansion.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Trap_Defense_Expansion-v1.2","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Trap_Defense_Expansion/Banner.png"},{"name": "Turret Variants","folder": "Turret_Variants","version": "3.1","description": "v3.1: Fixed 1 recipe outputs from D_ItemsStatic to D_ItemTemplate (crash fix). | Adds 15 new automated turret variants with unique characteristics.","category": "Combat & Defense","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Turret_Variants","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Turret_Variants/Turret_Variants.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Turret_Variants-v3.1","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Turret_Variants/Banner.png"},{"name": "UDA Terminal Laptop","folder": "UDA_Terminal_Laptop","version": "1.4","description": "v1.2: Placement fix. The laptop now deploys (shows a placement ghost) and the Press=Workshop / Hold=Orbital Deposit interactions fire. v1.1 used BP_Terminal_C (a lore-note BP that overrides Deploya...","category": "Uncategorized","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/UDA_Terminal_Laptop","download": "https://github.com/AgentKush/Icarus-mods/raw/main/UDA_Terminal_Laptop/UDA_Terminal_Laptop.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/UDA_Terminal_Laptop-v1.4","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/UDA_Terminal_Laptop/Banner.png"},{"name": "War Beasts","folder": "War_Beasts","version": "1.0","description": "The first taming-combat mod. Husbandry combat talents 3x stronger - turn tamed creatures into true war beasts that hit hard and survive fights.","category": "Uncategorized","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/War_Beasts","download": "https://github.com/AgentKush/Icarus-mods/raw/main/War_Beasts/War_Beasts.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/War_Beasts-v1.0","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/War_Beasts/Banner.png"},{"name": "Waste Not","folder": "Waste_Not","version": "2.2","description": "Mining yields useful secondary resources instead of Stone.","category": "Economy & Resources","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Waste_Not","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Waste_Not/Waste_Not.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Waste_Not-v2.2","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Waste_Not/Banner.png"},{"name": "Workshop Recyclers","folder": "Workshop_Recyclers","version": "5.7","description": "v5.5: Added 886 missing incinerate recipes (3054 total) - frozen items, ores, food, building pieces. Fixed icon + mesh + tech tree position. | Two recycling machines (Biofuel T3 + Organic T4) plus ...","category": "Workshop & Items","readme": "https://github.com/AgentKush/Icarus-mods/tree/main/Workshop_Recyclers","download": "https://github.com/AgentKush/Icarus-mods/raw/main/Workshop_Recyclers/Workshop_Recyclers.EXMODZ","release": "https://github.com/AgentKush/Icarus-mods/releases/tag/Workshop_Recyclers-v5.7","banner": "https://github.com/AgentKush/Icarus-mods/raw/main/Workshop_Recyclers/Banner.png"}];

const FEATURED_MODS=["Workshop_Recyclers","Agents_Individual_Item_Kits","Passive_Ore_Extractor_Drills"];
const CATEGORY_ICONS={"Workshop & Items":"🏪","Building & Construction":"🏗️","Processing Speed":"⚡","Combat & Defense":"⚔️","Survival & Difficulty":"💀","Economy & Resources":"💎","Food & Consumables":"🍖","Quality of Life":"✨","Mod Packs":"📦"};
const CATEGORY_ORDER=["Workshop & Items","Building & Construction","Processing Speed","Combat & Defense","Survival & Difficulty","Economy & Resources","Food & Consumables","Quality of Life","Mod Packs"];
let activeCategory=null;
let activeSort='category';
let downloadCounts={}; // populated by fetchDownloads

// --- CARD BANNER ART ---
function cardBanner(m){const i=m&&m.banner?`<img loading="lazy" src="${m.banner}" alt="" width="768" height="256">`:`<span class="mod-banner-ph">${(CATEGORY_ICONS[m.category]||'')}</span>`;return `<div class="mod-banner">${i}</div>`;}

// --- FEATURED ---
function renderFeatured(){
    const s=document.getElementById('featured-section');
    const f=MODS.filter(m=>FEATURED_MODS.includes(m.folder));
    if(!f.length)return;
    let h='<div class="featured-header"><span class="featured-star">⭐</span><h2>Popular Mods</h2><span class="featured-star">⭐</span></div><div class="featured-grid">';
    f.forEach(m=>{h+=`<div class="featured-card reveal"><div class="featured-badge">Popular</div>${cardBanner(m)}<div class="mod-name">${m.name}</div><div class="mod-desc">${m.description}</div><div class="mod-actions"><a href="${m.download}" class="download-btn">Download</a><a href="${m.readme}">README</a></div></div>`});
    h+='</div>';s.innerHTML=h;
}

// --- FILTER CHIPS ---
function renderChips(){
    const c=document.getElementById('filter-chips');
    let h='<span class="chip active" onclick="setCategory(null,this)">All</span>';
    CATEGORY_ORDER.forEach(cat=>{h+=`<span class="chip" onclick="setCategory('${cat}',this)">${CATEGORY_ICONS[cat]||''} ${cat}</span>`});
    c.innerHTML=h;
}

function setCategory(cat,el){
    activeCategory=cat;
    document.querySelectorAll('.chip').forEach(c=>c.classList.remove('active'));
    el.classList.add('active');
    filterMods(document.getElementById('search').value);
}

// --- CATALOG ---
function renderCatalog(mods){
    const catalog=document.getElementById('mod-catalog');
    const categories={};
    CATEGORY_ORDER.forEach(c=>{categories[c]=[]});
    mods.forEach(m=>{if(!categories[m.category])categories[m.category]=[];categories[m.category].push(m)});
    let html='';
    for(const cat of CATEGORY_ORDER){
        const cm=categories[cat];if(!cm||!cm.length)continue;
        const icon=CATEGORY_ICONS[cat]||"📁";
        html+=`<div class="category reveal" data-category="${cat}"><div class="category-header"><div class="category-icon">${icon}</div><h2>${cat}</h2><span class="category-count">${cm.length} mods</span></div><div class="mod-grid stagger-children">`;
        cm.forEach(m=>{html+=`<div class="mod-card reveal" data-name="${m.name.toLowerCase()}" data-desc="${m.description.toLowerCase()}" data-folder="${m.folder}" data-category="${m.category}">${cardBanner(m)}<div class="mod-header"><span class="mod-name">${m.name}</span><span class="mod-version">v${m.version}</span></div><div class="mod-meta"><span class="download-count" id="dl-${m.folder}"></span></div><div class="mod-desc">${m.description}</div><div class="mod-actions"><a href="${m.download}" class="download-btn">Download</a><a href="${m.readme}">README</a><a href="${m.release}">Release</a></div></div>`});
        html+='</div></div>';
    }
    catalog.innerHTML=html;
    observeRevealElements();
}

// --- SEARCH + FILTER ---
function filterMods(q){
    q=q.toLowerCase().trim();let any=false;
    document.querySelectorAll('.mod-card').forEach(c=>{
        const n=c.dataset.name,d=c.dataset.desc,cat=c.dataset.category;
        const v=(!q||n.includes(q)||d.includes(q))&&(!activeCategory||cat===activeCategory);
        c.classList.toggle('hidden',!v);if(v)any=true;
    });
    document.querySelectorAll('.category').forEach(c=>{c.classList.toggle('hidden',c.querySelectorAll('.mod-card:not(.hidden)').length===0)});
    document.getElementById('no-results').classList.toggle('hidden',any);
    pushURLState(q);
    updateAutocomplete(q);
}

// --- URL STATE (shareable links) ---
function pushURLState(q) {
    const params = new URLSearchParams();
    if (activeCategory) params.set('category', activeCategory);
    if (q) params.set('q', q);
    if (activeSort !== 'category') params.set('sort', activeSort);
    const qs = params.toString();
    const url = qs ? `${location.pathname}?${qs}` : location.pathname;
    history.replaceState(null, '', url);
}

function restoreURLState() {
    const params = new URLSearchParams(location.search);
    const cat = params.get('category');
    const q = params.get('q') || '';
    const sort = params.get('sort') || 'category';

    if (q) {
        document.getElementById('search').value = q;
    }
    if (cat && CATEGORY_ORDER.includes(cat)) {
        activeCategory = cat;
        document.querySelectorAll('.chip').forEach(c => {
            const isMatch = c.textContent.includes(cat);
            c.classList.toggle('active', isMatch);
            if (c.textContent === 'All') c.classList.toggle('active', !cat);
        });
    }
    if (sort !== 'category') {
        activeSort = sort;
        const sel = document.getElementById('sort-select');
        if (sel) sel.value = sort;
        applySort(sort);
    }
    if (q || cat) filterMods(q);
}

// --- SCROLL ANIMATIONS ---
function observeRevealElements(){
    const o=new IntersectionObserver(e=>{e.forEach(en=>{if(en.isIntersecting)en.target.classList.add('visible')})},{threshold:.05,rootMargin:'0px 0px -40px 0px'});
    document.querySelectorAll('.reveal:not(.visible)').forEach(el=>o.observe(el));
}

// --- NAVBAR + BACK TO TOP (throttled for perf) ---
let scrollTicking = false;
window.addEventListener('scroll', () => {
    if (!scrollTicking) {
        scrollTicking = true;
        requestAnimationFrame(() => {
            document.getElementById('navbar').classList.toggle('scrolled', window.scrollY > 100);
            document.getElementById('backToTop').classList.toggle('show', window.scrollY > 400);
            scrollTicking = false;
        });
    }
}, { passive: true });

// --- DOWNLOAD COUNTS ---
async function fetchDownloads(){
    let p=1,all=[];
    while(true){try{const r=await fetch(`https://api.github.com/repos/AgentKush/Icarus-mods/releases?per_page=100&page=${p}`);if(!r.ok)break;const d=await r.json();if(!d.length)break;all=all.concat(d);if(d.length<100)break;p++}catch(e){break}}
    let total=0;
    all.forEach(r=>{const f=(r.tag_name||'').replace(/-v[\d.]+$/,'');const dl=(r.assets||[]).reduce((s,a)=>s+(a.download_count||0),0);downloadCounts[f]=(downloadCounts[f]||0)+dl;total+=dl});
    MODS.forEach(m=>{const el=document.getElementById('dl-'+m.folder);if(el){const c=downloadCounts[m.folder]||0;el.textContent=c>0?c.toLocaleString()+' downloads':''}});
    const dlEl=document.getElementById('dl-total');if(dlEl){dlEl.textContent=total>0?total.toLocaleString():'—'}
}

// --- COUNTING ANIMATION (Zayon suggestion) ---
function animateCounters() {
    document.querySelectorAll('.number[data-count]').forEach(el => {
        const target = parseInt(el.dataset.count);
        const suffix = '+';
        const duration = 1000;
        const start = performance.now();
        function update(now) {
            const elapsed = now - start;
            const progress = Math.min(elapsed / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = Math.floor(eased * target);
            el.textContent = current.toLocaleString() + (progress >= 1 ? suffix : '');
            if (progress < 1) requestAnimationFrame(update);
        }
        requestAnimationFrame(update);
    });
}

/* ═══════════════════════════════════════════
   PREMIUM EFFECTS
   ═══════════════════════════════════════════ */

// --- TEXT SCRAMBLE HERO ---
function textScramble(el, finalText) {
    const chars = '!<>-_\\/[]{}—=+*^?#________';
    let frame = 0;
    const totalFrames = finalText.length * 3;
    const revealed = [];

    // Start with empty and build up
    for (let i = 0; i < finalText.length; i++) {
        revealed.push({ char: '', done: false, revealAt: Math.floor(Math.random() * totalFrames * 0.7) + 4 });
    }

    // Add blinking cursor span
    const cursor = document.createElement('span');
    cursor.className = 'scramble-cursor';
    cursor.textContent = '';

    function tick() {
        let output = '';
        let allDone = true;

        for (let i = 0; i < finalText.length; i++) {
            if (frame >= revealed[i].revealAt) {
                revealed[i].done = true;
                revealed[i].char = finalText[i];
            } else {
                allDone = false;
                revealed[i].char = chars[Math.floor(Math.random() * chars.length)];
            }
            output += revealed[i].char;
        }

        el.textContent = output;
        el.appendChild(cursor);
        frame++;

        if (!allDone && frame < totalFrames + 10) {
            requestAnimationFrame(tick);
        } else {
            // Final state: clean text + cursor
            el.textContent = finalText;
            el.appendChild(cursor);
        }
    }

    // Clear and start
    el.textContent = '';
    el.appendChild(cursor);
    requestAnimationFrame(tick);
}

// --- SPOTLIGHT CURSOR (hero section only) ---
function initSpotlightCursor() {
    const hero = document.getElementById('hero');
    const spotlight = document.getElementById('heroSpotlight');
    if (!hero || !spotlight) return;

    // Only active on desktop
    if (window.innerWidth < 768) return;

    hero.addEventListener('mousemove', (e) => {
        spotlight.style.left = e.clientX + 'px';
        spotlight.style.top = e.clientY + 'px';
        spotlight.style.opacity = '1';
    });

    hero.addEventListener('mouseleave', () => {
        spotlight.style.opacity = '0';
    });
}

// --- MAGNETIC BUTTONS ---
function initMagneticButtons() {
    if (window.innerWidth < 768) return;

    const buttons = document.querySelectorAll('.magnetic-btn');
    const PULL_DISTANCE = 80;  // px radius of influence
    const PULL_STRENGTH = 0.3; // multiplier

    buttons.forEach(btn => {
        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            const cx = rect.left + rect.width / 2;
            const cy = rect.top + rect.height / 2;
            const dx = e.clientX - cx;
            const dy = e.clientY - cy;
            const dist = Math.sqrt(dx * dx + dy * dy);

            if (dist < PULL_DISTANCE) {
                const tx = dx * PULL_STRENGTH;
                const ty = dy * PULL_STRENGTH;
                btn.style.transform = `translate(${tx}px, ${ty}px)`;
            }
        });

        btn.addEventListener('mouseleave', () => {
            btn.style.transform = '';
        });
    });
}

// --- CARD CURSOR-FOLLOW GLOW ---
function initCardGlow() {
    if (window.innerWidth < 768) return;

    // Use event delegation on the catalog container for better perf
    const catalog = document.getElementById('mod-catalog');
    const featured = document.getElementById('featured-section');

    function handleCardMove(e) {
        const card = e.target.closest('.mod-card, .featured-card');
        if (!card) return;
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        card.style.setProperty('--mouse-x', x + 'px');
        card.style.setProperty('--mouse-y', y + 'px');
    }

    if (catalog) catalog.addEventListener('mousemove', handleCardMove, { passive: true });
    if (featured) featured.addEventListener('mousemove', handleCardMove, { passive: true });
}

// --- VANILLA TILT INIT ---
function initVanillaTilt() {
    if (typeof VanillaTilt === 'undefined') return;
    if (window.innerWidth < 768) return;

    // Mod cards — subtle tilt
    const modCards = document.querySelectorAll('.mod-card');
    if (modCards.length) {
        VanillaTilt.init(modCards, {
            max: 4,
            speed: 400,
            glare: false,
            'max-glare': 0,
            perspective: 1200,
            gyroscope: false
        });
    }

    // Featured cards — slightly more dramatic
    const featuredCards = document.querySelectorAll('.featured-card');
    if (featuredCards.length) {
        VanillaTilt.init(featuredCards, {
            max: 6,
            speed: 400,
            glare: true,
            'max-glare': 0.08,
            perspective: 1000,
            gyroscope: false
        });
    }
}

// --- SCROLL PROGRESS BAR (inject into DOM) ---
function initScrollProgress() {
    // Check if CSS scroll-driven animations are supported
    if (!CSS.supports || !CSS.supports('animation-timeline', 'scroll(root)')) return;

    // Only inject if not already present
    if (document.querySelector('.scroll-progress')) return;

    const bar = document.createElement('div');
    bar.className = 'scroll-progress';
    bar.setAttribute('aria-hidden', 'true');
    document.body.prepend(bar);
}

// --- REDUCED MOTION CHECK ---
function prefersReducedMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

/* ═══════════════════════════════════════════
   SORT, AUTOCOMPLETE, MODAL, KEYBOARD
   ═══════════════════════════════════════════ */

// --- SORT ---
function applySort(sortBy) {
    activeSort = sortBy;
    const catalog = document.getElementById('mod-catalog');
    if (sortBy === 'category') {
        // Re-render default category layout
        renderCatalog(MODS);
        filterMods(document.getElementById('search').value);
        return;
    }

    // Flat sort: collect all visible mod cards into a single grid
    let sorted = [...MODS];
    if (sortBy === 'name') {
        sorted.sort((a, b) => a.name.localeCompare(b.name));
    } else if (sortBy === 'downloads') {
        sorted.sort((a, b) => (downloadCounts[b.folder] || 0) - (downloadCounts[a.folder] || 0));
    } else if (sortBy === 'version') {
        sorted.sort((a, b) => {
            const pa = a.version.split('.').map(Number);
            const pb = b.version.split('.').map(Number);
            for (let i = 0; i < Math.max(pa.length, pb.length); i++) {
                const diff = (pb[i] || 0) - (pa[i] || 0);
                if (diff !== 0) return diff;
            }
            return 0;
        });
    }

    let html = '<div class="mod-grid stagger-children">';
    sorted.forEach(m => {
        html += `<div class="mod-card reveal" data-name="${m.name.toLowerCase()}" data-desc="${m.description.toLowerCase()}" data-folder="${m.folder}" data-category="${m.category}">${cardBanner(m)}<div class="mod-header"><span class="mod-name">${m.name}</span><span class="mod-version">v${m.version}</span></div><div class="mod-meta"><span class="download-count" id="dl-${m.folder}">${downloadCounts[m.folder] ? downloadCounts[m.folder].toLocaleString() + ' downloads' : ''}</span></div><div class="mod-desc">${m.description}</div><div class="mod-actions"><a href="${m.download}" class="download-btn">Download</a><a href="${m.readme}">README</a><a href="${m.release}">Release</a></div></div>`;
    });
    html += '</div>';
    catalog.innerHTML = html;
    observeRevealElements();
    filterMods(document.getElementById('search').value);
    pushURLState(document.getElementById('search').value);
}

// --- AUTOCOMPLETE ---
let acIndex = -1; // active autocomplete index

function updateAutocomplete(q) {
    const dropdown = document.getElementById('autocomplete');
    if (!dropdown) return;

    if (!q || q.length < 2) {
        dropdown.classList.add('hidden');
        dropdown.innerHTML = '';
        acIndex = -1;
        return;
    }

    const matches = MODS.filter(m =>
        m.name.toLowerCase().includes(q) || m.description.toLowerCase().includes(q)
    ).slice(0, 6);

    if (!matches.length) {
        dropdown.classList.add('hidden');
        dropdown.innerHTML = '';
        acIndex = -1;
        return;
    }

    dropdown.innerHTML = matches.map((m, i) => {
        // Highlight matching text in name
        const nameHtml = highlightMatch(m.name, q);
        return `<div class="autocomplete-item" role="option" data-index="${i}" onclick="selectAutocomplete('${m.name.replace(/'/g, "\\'")}')">${nameHtml}<span class="ac-category">${CATEGORY_ICONS[m.category] || ''} ${m.category}</span></div>`;
    }).join('');

    dropdown.classList.remove('hidden');
    acIndex = -1;
}

function highlightMatch(text, query) {
    const idx = text.toLowerCase().indexOf(query.toLowerCase());
    if (idx === -1) return text;
    return text.substring(0, idx) + '<mark>' + text.substring(idx, idx + query.length) + '</mark>' + text.substring(idx + query.length);
}

function selectAutocomplete(name) {
    const search = document.getElementById('search');
    search.value = name;
    filterMods(name);
    document.getElementById('autocomplete').classList.add('hidden');
    search.focus();
}

function navigateAutocomplete(direction) {
    const items = document.querySelectorAll('.autocomplete-item');
    if (!items.length) return;
    items.forEach(i => i.classList.remove('active'));
    acIndex += direction;
    if (acIndex < 0) acIndex = items.length - 1;
    if (acIndex >= items.length) acIndex = 0;
    items[acIndex].classList.add('active');
    items[acIndex].scrollIntoView({ block: 'nearest' });
}

// --- MOD DETAIL MODAL ---
function createModal() {
    if (document.getElementById('mod-modal')) return;
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.id = 'mod-modal';
    overlay.innerHTML = '<div class="modal-content" role="dialog" aria-modal="true"><button class="modal-close" aria-label="Close" onclick="closeModal()">&times;</button><div id="modal-body"></div></div>';
    document.body.appendChild(overlay);

    // Close on overlay click
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) closeModal();
    });
}

function openModal(folder) {
    const mod = MODS.find(m => m.folder === folder);
    if (!mod) return;

    createModal();
    const body = document.getElementById('modal-body');
    const dl = downloadCounts[folder] || 0;

    body.innerHTML = `
        ${mod.banner ? `<div class="modal-banner"><img loading="lazy" src="${mod.banner}" alt="" width="768" height="256"></div>` : ''}
        <div class="modal-title">${mod.name}</div>
        <span class="modal-version">v${mod.version}</span>
        <div class="modal-category">${CATEGORY_ICONS[mod.category] || ''} ${mod.category}</div>
        ${dl > 0 ? `<div class="modal-downloads">${dl.toLocaleString()} downloads</div>` : ''}
        <div class="modal-desc">${mod.description}</div>
        <div class="modal-actions">
            <a href="${mod.download}" class="download-btn">Download</a>
            <a href="${mod.readme}">README</a>
            <a href="${mod.release}">Release</a>
        </div>
    `;

    const modal = document.getElementById('mod-modal');
    modal.classList.add('open');
    document.body.style.overflow = 'hidden';

    // Focus trap: focus close button
    modal.querySelector('.modal-close').focus();
}

function closeModal() {
    const modal = document.getElementById('mod-modal');
    if (modal) {
        modal.classList.remove('open');
        document.body.style.overflow = '';
    }
}

// Click handler for mod cards — open modal on card body click (not action links)
function initCardClickModal() {
    document.addEventListener('click', (e) => {
        // Don't trigger modal if clicking a link/button
        if (e.target.closest('a, button')) return;
        const card = e.target.closest('.mod-card');
        if (card && card.dataset.folder) {
            openModal(card.dataset.folder);
        }
    });
}

// --- KEYBOARD SHORTCUTS ---
function initKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        const search = document.getElementById('search');
        const modal = document.getElementById('mod-modal');
        const dropdown = document.getElementById('autocomplete');
        const isSearchFocused = document.activeElement === search;

        // Escape: close modal or clear search
        if (e.key === 'Escape') {
            if (modal && modal.classList.contains('open')) {
                closeModal();
                e.preventDefault();
                return;
            }
            if (isSearchFocused) {
                search.value = '';
                filterMods('');
                search.blur();
                e.preventDefault();
                return;
            }
            if (dropdown && !dropdown.classList.contains('hidden')) {
                dropdown.classList.add('hidden');
                e.preventDefault();
                return;
            }
        }

        // "/" to focus search (when not already in an input)
        if (e.key === '/' && !isSearchFocused && !e.ctrlKey && !e.metaKey) {
            const tag = document.activeElement?.tagName;
            if (tag !== 'INPUT' && tag !== 'TEXTAREA' && tag !== 'SELECT') {
                e.preventDefault();
                search.focus();
                search.select();
            }
        }

        // Arrow keys in autocomplete
        if (isSearchFocused && dropdown && !dropdown.classList.contains('hidden')) {
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                navigateAutocomplete(1);
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                navigateAutocomplete(-1);
            } else if (e.key === 'Enter' && acIndex >= 0) {
                e.preventDefault();
                const items = document.querySelectorAll('.autocomplete-item');
                if (items[acIndex]) items[acIndex].click();
            }
        }
    });

    // Close autocomplete on click outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.nav-search')) {
            const dropdown = document.getElementById('autocomplete');
            if (dropdown) dropdown.classList.add('hidden');
        }
    });
}

// --- UPDATE NOTIFICATIONS (new mods since last visit) ---
function checkForUpdates() {
    const STORAGE_KEY = 'ak_last_mod_count';
    try {
        const lastCount = parseInt(localStorage.getItem(STORAGE_KEY) || '0');
        const currentCount = MODS.length;

        if (lastCount > 0 && currentCount > lastCount) {
            const diff = currentCount - lastCount;
            showUpdateBanner(diff);
        }
        localStorage.setItem(STORAGE_KEY, currentCount.toString());
    } catch (e) {
        // localStorage not available, skip silently
    }
}

function showUpdateBanner(count) {
    const banner = document.createElement('div');
    banner.className = 'update-banner';
    banner.innerHTML = `<span>🆕 ${count} new mod${count > 1 ? 's' : ''} since your last visit!</span><button onclick="this.parentElement.remove()" aria-label="Dismiss">&times;</button>`;
    // Insert after navbar
    const nav = document.getElementById('navbar');
    if (nav) nav.after(banner);
    // Auto-dismiss after 10s
    setTimeout(() => { if (banner.parentElement) banner.remove(); }, 10000);
}

// --- FAVORITES SYSTEM ---
const FAVORITES_KEY = 'ak_favorites';

function getFavorites() {
    try {
        return JSON.parse(localStorage.getItem(FAVORITES_KEY) || '[]');
    } catch { return []; }
}

function saveFavorites(favs) {
    try { localStorage.setItem(FAVORITES_KEY, JSON.stringify(favs)); } catch {}
}

function toggleFavorite(folder, e) {
    if (e) { e.stopPropagation(); e.preventDefault(); }
    let favs = getFavorites();
    if (favs.includes(folder)) {
        favs = favs.filter(f => f !== folder);
    } else {
        favs.push(folder);
    }
    saveFavorites(favs);
    // Update all heart icons for this folder
    document.querySelectorAll(`.fav-btn[data-folder="${folder}"]`).forEach(btn => {
        btn.classList.toggle('favorited', favs.includes(folder));
        btn.setAttribute('aria-label', favs.includes(folder) ? 'Remove from favorites' : 'Add to favorites');
    });
    updateFavChipCount();
}

function updateFavChipCount() {
    const chip = document.getElementById('fav-chip');
    if (!chip) return;
    const count = getFavorites().length;
    chip.textContent = count > 0 ? `❤ Favorites (${count})` : '❤ Favorites';
}

function isFavorited(folder) {
    return getFavorites().includes(folder);
}

// --- MOD COMPARISON ---
let compareList = [];

function toggleCompare(folder, e) {
    if (e) { e.stopPropagation(); e.preventDefault(); }
    const idx = compareList.indexOf(folder);
    if (idx >= 0) {
        compareList.splice(idx, 1);
    } else if (compareList.length < 3) {
        compareList.push(folder);
    } else {
        return; // max 3
    }
    // Update button states
    document.querySelectorAll(`.compare-btn[data-folder="${folder}"]`).forEach(btn => {
        btn.classList.toggle('comparing', compareList.includes(folder));
    });
    updateCompareBar();
}

function updateCompareBar() {
    let bar = document.getElementById('compare-bar');
    if (compareList.length === 0) {
        if (bar) bar.remove();
        return;
    }
    if (!bar) {
        bar = document.createElement('div');
        bar.className = 'compare-bar';
        bar.id = 'compare-bar';
        document.body.appendChild(bar);
    }
    const names = compareList.map(f => {
        const mod = MODS.find(m => m.folder === f);
        return mod ? mod.name : f;
    });
    bar.innerHTML = `<span>Comparing: ${names.join(' vs ')}</span><div class="compare-bar-actions"><button onclick="openCompareModal()">Compare Now</button><button onclick="clearCompare()" class="compare-clear">Clear</button></div>`;
}

function clearCompare() {
    compareList.forEach(f => {
        document.querySelectorAll(`.compare-btn[data-folder="${f}"]`).forEach(btn => btn.classList.remove('comparing'));
    });
    compareList = [];
    updateCompareBar();
}

function openCompareModal() {
    if (compareList.length < 2) return;
    createModal();
    const body = document.getElementById('modal-body');
    const mods = compareList.map(f => MODS.find(m => m.folder === f)).filter(Boolean);

    let html = '<div class="modal-title" style="margin-bottom:16px">Mod Comparison</div>';
    html += '<div class="compare-grid" style="display:grid;grid-template-columns:repeat(' + mods.length + ',1fr);gap:16px">';
    mods.forEach(m => {
        const dl = downloadCounts[m.folder] || 0;
        html += `<div class="compare-col">
            <div style="font-weight:700;color:#fff;margin-bottom:6px;font-size:0.95rem">${m.name}</div>
            <div class="modal-version" style="margin-bottom:8px">v${m.version}</div>
            <div style="font-size:0.78rem;color:var(--text-muted);margin-bottom:8px">${CATEGORY_ICONS[m.category]||''} ${m.category}</div>
            ${dl > 0 ? `<div style="font-size:0.82rem;color:var(--accent);margin-bottom:10px">${dl.toLocaleString()} downloads</div>` : ''}
            <div style="font-size:0.82rem;color:var(--text-secondary);line-height:1.55;margin-bottom:12px">${m.description}</div>
            <a href="${m.download}" class="download-btn" style="font-size:0.78rem;padding:6px 14px;border-radius:4px;display:inline-block;background:var(--accent);color:#fff;font-weight:600">Download</a>
        </div>`;
    });
    html += '</div>';
    body.innerHTML = html;

    const modal = document.getElementById('mod-modal');
    modal.classList.add('open');
    // Widen modal for comparison
    modal.querySelector('.modal-content').style.maxWidth = (mods.length * 260 + 80) + 'px';
    document.body.style.overflow = 'hidden';
    modal.querySelector('.modal-close').focus();
}

// Override closeModal to reset width
const _origCloseModal = closeModal;
closeModal = function() {
    const modal = document.getElementById('mod-modal');
    if (modal) {
        modal.classList.remove('open');
        document.body.style.overflow = '';
        const content = modal.querySelector('.modal-content');
        if (content) content.style.maxWidth = '';
    }
};

// --- CHANGELOG / WHAT'S NEW ---
function renderChangelog() {
    const section = document.getElementById('changelog-section');
    if (!section) return;

    // Fetch recent releases to build a "What's New" feed
    fetch('https://api.github.com/repos/AgentKush/Icarus-mods/releases?per_page=8')
        .then(r => r.ok ? r.json() : [])
        .then(releases => {
            if (!releases.length) { section.classList.add('hidden'); return; }

            let html = '<div class="changelog-header"><h2>What\'s New</h2></div><div class="changelog-list">';
            releases.slice(0, 6).forEach(r => {
                const name = r.name || r.tag_name || 'Update';
                const date = new Date(r.published_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
                const body = (r.body || '').split('\n').filter(l => l.trim()).slice(0, 3).join(' ').substring(0, 150);
                html += `<div class="changelog-item reveal"><div class="changelog-date">${date}</div><div class="changelog-name">${name}</div>${body ? `<div class="changelog-body">${body}${body.length >= 150 ? '...' : ''}</div>` : ''}</div>`;
            });
            html += '</div>';
            section.innerHTML = html;
            section.classList.remove('hidden');
            observeRevealElements();
        })
        .catch(() => { section.classList.add('hidden'); });
}

// --- INJECT FAVORITE + COMPARE BUTTONS INTO CARD RENDERING ---
// Override renderCatalog to include fav/compare buttons
const _origRenderCatalog = renderCatalog;
renderCatalog = function(mods) {
    const catalog = document.getElementById('mod-catalog');
    const categories = {};
    CATEGORY_ORDER.forEach(c => { categories[c] = []; });
    mods.forEach(m => { if (!categories[m.category]) categories[m.category] = []; categories[m.category].push(m); });
    let html = '';
    for (const cat of CATEGORY_ORDER) {
        const cm = categories[cat]; if (!cm || !cm.length) continue;
        const icon = CATEGORY_ICONS[cat] || "📁";
        html += `<div class="category reveal" data-category="${cat}"><div class="category-header"><div class="category-icon">${icon}</div><h2>${cat}</h2><span class="category-count">${cm.length} mods</span></div><div class="mod-grid stagger-children">`;
        cm.forEach(m => {
            const faved = isFavorited(m.folder);
            html += `<div class="mod-card reveal" data-name="${m.name.toLowerCase()}" data-desc="${m.description.toLowerCase()}" data-folder="${m.folder}" data-category="${m.category}">${cardBanner(m)}<div class="mod-header"><span class="mod-name">${m.name}</span><div class="mod-header-actions"><button class="fav-btn${faved ? ' favorited' : ''}" data-folder="${m.folder}" onclick="toggleFavorite('${m.folder}',event)" aria-label="${faved ? 'Remove from favorites' : 'Add to favorites'}" data-tooltip="${faved ? 'Unfavorite' : 'Favorite'}">♥</button><button class="compare-btn${compareList.includes(m.folder) ? ' comparing' : ''}" data-folder="${m.folder}" onclick="toggleCompare('${m.folder}',event)" aria-label="Compare mods" data-tooltip="Compare">⚖</button><span class="mod-version">v${m.version}</span></div></div><div class="mod-meta"><span class="download-count" id="dl-${m.folder}"></span></div><div class="mod-desc">${m.description}</div><div class="mod-actions"><a href="${m.download}" class="download-btn">Download</a><a href="${m.readme}">README</a><a href="${m.release}">Release</a></div></div>`;
        });
        html += '</div></div>';
    }
    catalog.innerHTML = html;
    observeRevealElements();
};

// Also update applySort to include fav/compare buttons in flat mode
const _origApplySort = applySort;
applySort = function(sortBy) {
    activeSort = sortBy;
    if (sortBy === 'category') {
        renderCatalog(MODS);
        filterMods(document.getElementById('search').value);
        return;
    }
    let sorted = [...MODS];
    if (sortBy === 'name') sorted.sort((a, b) => a.name.localeCompare(b.name));
    else if (sortBy === 'downloads') sorted.sort((a, b) => (downloadCounts[b.folder] || 0) - (downloadCounts[a.folder] || 0));
    else if (sortBy === 'version') {
        sorted.sort((a, b) => {
            const pa = a.version.split('.').map(Number), pb = b.version.split('.').map(Number);
            for (let i = 0; i < Math.max(pa.length, pb.length); i++) { const d = (pb[i]||0) - (pa[i]||0); if (d !== 0) return d; } return 0;
        });
    }
    const catalog = document.getElementById('mod-catalog');
    let html = '<div class="mod-grid stagger-children">';
    sorted.forEach(m => {
        const faved = isFavorited(m.folder);
        html += `<div class="mod-card reveal" data-name="${m.name.toLowerCase()}" data-desc="${m.description.toLowerCase()}" data-folder="${m.folder}" data-category="${m.category}">${cardBanner(m)}<div class="mod-header"><span class="mod-name">${m.name}</span><div class="mod-header-actions"><button class="fav-btn${faved ? ' favorited' : ''}" data-folder="${m.folder}" onclick="toggleFavorite('${m.folder}',event)" aria-label="${faved ? 'Remove from favorites' : 'Add to favorites'}" data-tooltip="${faved ? 'Unfavorite' : 'Favorite'}">♥</button><button class="compare-btn${compareList.includes(m.folder) ? ' comparing' : ''}" data-folder="${m.folder}" onclick="toggleCompare('${m.folder}',event)" aria-label="Compare mods" data-tooltip="Compare">⚖</button><span class="mod-version">v${m.version}</span></div></div><div class="mod-meta"><span class="download-count" id="dl-${m.folder}">${downloadCounts[m.folder] ? downloadCounts[m.folder].toLocaleString() + ' downloads' : ''}</span></div><div class="mod-desc">${m.description}</div><div class="mod-actions"><a href="${m.download}" class="download-btn">Download</a><a href="${m.readme}">README</a><a href="${m.release}">Release</a></div></div>`;
    });
    html += '</div>';
    catalog.innerHTML = html;
    observeRevealElements();
    filterMods(document.getElementById('search').value);
    pushURLState(document.getElementById('search').value);
};

// Update renderChips to add Favorites chip
const _origRenderChips = renderChips;
renderChips = function() {
    const c = document.getElementById('filter-chips');
    const favCount = getFavorites().length;
    let h = '<span class="chip active" onclick="setCategory(null,this)">All</span>';
    h += `<span class="chip chip-fav" id="fav-chip" onclick="setCategory('__favorites__',this)">❤ Favorites${favCount > 0 ? ' (' + favCount + ')' : ''}</span>`;
    CATEGORY_ORDER.forEach(cat => { h += `<span class="chip" onclick="setCategory('${cat}',this)">${CATEGORY_ICONS[cat]||''} ${cat}</span>`; });
    c.innerHTML = h;
};

// Update filterMods to handle favorites pseudo-category
const _origFilterMods = filterMods;
filterMods = function(q) {
    q = q.toLowerCase().trim();
    let any = false;
    const favs = getFavorites();
    document.querySelectorAll('.mod-card').forEach(c => {
        const n = c.dataset.name, d = c.dataset.desc, cat = c.dataset.category, folder = c.dataset.folder;
        let catMatch = !activeCategory || cat === activeCategory;
        if (activeCategory === '__favorites__') catMatch = favs.includes(folder);
        const v = (!q || n.includes(q) || d.includes(q)) && catMatch;
        c.classList.toggle('hidden', !v);
        if (v) any = true;
    });
    document.querySelectorAll('.category').forEach(c => { c.classList.toggle('hidden', c.querySelectorAll('.mod-card:not(.hidden)').length === 0); });
    document.getElementById('no-results').classList.toggle('hidden', any);
    pushURLState(q);
    updateAutocomplete(q);
};

// --- INIT ---
renderFeatured();
renderChips();
renderCatalog(MODS);
fetchDownloads();
document.querySelectorAll('.hero .reveal').forEach(el => el.classList.add('visible'));
animateCounters();

// New features
initCardClickModal();
initKeyboardShortcuts();
restoreURLState();
checkForUpdates();
renderChangelog();

// --- SERVICE WORKER REGISTRATION ---
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('./sw.js').catch(() => {});
    });
}

// Premium effects (respect reduced motion)
if (!prefersReducedMotion()) {
    // Scramble the hero title for that hacker-terminal feel
    const heroTitle = document.getElementById('hero-title');
    if (heroTitle) {
        textScramble(heroTitle, 'AGENTKUSH');
    }

    initSpotlightCursor();
    initMagneticButtons();
    initCardGlow();
    initScrollProgress();

    // Vanilla Tilt — slight delay to ensure DOM is fully painted
    requestAnimationFrame(() => {
        initVanillaTilt();
    });
}
