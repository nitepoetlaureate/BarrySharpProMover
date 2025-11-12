# Barry Sharp's Pro Mover - Art Style Guide

**Version:** 1.0
**Date:** November 12, 2025
**Status:** DRAFT - To be expanded during Phase 1

---

## Platform Constraints

### Game Boy Color Specifications
- Resolution: 160x144 pixels
- Tile size: 8x8 pixels
- Sprites: Up to 40 sprites on screen, max 10 per scanline
- Sprite sizes: 8x8 or 8x16 pixels
- Background: 32x32 tile grid
- Colors: Up to 56 colors from palette of 32,768
- Palettes: 8 background palettes, 8 sprite palettes (4 colors each)

### Technical Limits (GB Studio)
- Max sprites per scene: Varies by complexity
- Max background tiles: 192 unique tiles per scene
- Animation frames: 4-8 frames typical for character animations
- File formats: PNG with transparency

---

## Visual Style

### Overall Aesthetic
- **Authentic retro:** True to GBC era, not "modern retro"
- **Readable:** Clear silhouettes, distinct characters even at small size
- **Expressive:** Characters convey personality through posture and animation
- **Philadelphia character:** Gritty, real, authentic to the city
- **Humor in details:** Visual gags and references for observant players

### Artistic Influences
- Classic GBC games: Pokemon Crystal, Legend of Zelda Oracle series, Wario Land 3
- Pixel art masters: Paul Robertson, eBoy, Mojang (early Minecraft aesthetic)
- Philadelphia itself: Row homes, brick, street art, working-class aesthetic

---

## Color Palette

### Primary Palette (Outdoor/Day)
```
Background:
- #F8E8C8 (Cream/highlight)
- #D89048 (Brown/mid)
- #A85820 (Dark brown)
- #301850 (Purple-black/shadow)

Sprites:
- #F8F8F8 (White/highlight)
- #D8B0A0 (Skin tone)
- #906040 (Brown)
- #281828 (Near-black)
```

### Secondary Palette (Indoor/Night)
```
Background:
- #A8D0A8 (Pale green)
- #607858 (Green-gray)
- #385040 (Dark green)
- #182028 (Blue-black)

Sprites:
- #F8E0B8 (Warm highlight)
- #C89858 (Wood/tan)
- #705030 (Dark brown)
- #201018 (Black)
```

### Accent Palette (UI/Special)
```
Cash: #40E840 (Bright green)
Danger: #E84040 (Bright red)
Info: #48B8F8 (Bright blue)
Party: #F848F8 (Bright magenta)
```

**Note:** All colors subject to adjustment for GBC hardware palette constraints.

---

## Character Sprites

### Barry Sharp (Player Character)
**Size:** 16x16 pixels (2x2 tiles)
**Palette:** Primary sprite palette

**States Required:**
- Idle (2-4 frame loop)
- Walk (4 frames, 8-directional or 4-directional)
- Carry light (walking with small item)
- Carry heavy (walking with large item, slower)
- Strain (trying to lift too-heavy item)
- Celebrate (job complete)
- Ouch (take damage/drop item)

**Design Notes:**
- Distinctive silhouette (possibly hat, work clothes)
- Clear which direction facing
- Visible weight/strain when carrying
- Expressive even at small size

### Coworker Characters
**Size:** 16x16 pixels
**Count:** 3-5 unique characters

**Required Coworkers:**
1. Veteran mover (experienced, older)
2. Rookie (nervous, learning)
3. Party animal (fun-loving, wild)
4. Specialist (technical, particular)
5. (Optional) Boss character

**Each Needs:**
- Idle pose
- Walk cycle (2-4 frames minimum)
- Portrait for dialogue (if using portraits)
- Distinct color palette and silhouette

### Customer Characters
**Size:** 16x16 pixels
**Count:** 8-12 unique types

**Archetypes:**
- Wealthy homeowner
- College student
- Elderly person
- Business owner
- Artist
- Paranoid person
- Friendly helper
- Difficult customer

**Variation:**
- Each type can have 2-3 palette swaps for variety
- Minimal animation (idle + gesture)

---

## Furniture & Object Sprites

### Furniture Size Categories

**Small Items (8x8 or 8x16):**
- Box
- Lamp
- Small plant
- Books
- Kitchen items

**Medium Items (16x16):**
- Chair
- Small table
- Nightstand
- TV
- Microwave

**Large Items (16x24 or 24x24):**
- Couch
- Bed
- Dresser
- Large table
- Refrigerator

**Awkward Items (Special sprites):**
- Piano (32x24 - requires 2 movers)
- Tall bookshelf (16x32 - vertical challenge)
- Glass items (breakable indicator)

### Visual Weight Indicators
- Light items: Clean lines, simple
- Medium items: More detail, substance
- Heavy items: Thick lines, solid appearance
- Awkward items: Unusual proportions, warning color accent

---

## Background Art

### Interior Locations

**Apartment Types:**
- Studio (single room)
- Row home (multiple floors, stairs)
- High-rise (elevator required)
- House (suburban, front/back yard)

**Business Locations:**
- Office (cubicles, desks)
- Restaurant (kitchen hazards)
- Store (narrow aisles)

**Tile Usage:**
- Reuse tiles across locations
- Modular wall/floor pieces
- Variation through palette swaps

### Exterior Locations

**Philadelphia Streets:**
- Row home facades (brick, varied colors)
- Street parking (cars, meters, danger zones)
- Sidewalks (varying width)
- Alleys (narrow, truck access)

**Landmarks (Simplified):**
- City Hall (recognizable but small)
- Art Museum steps (if included)
- South Street vibe (murals, color)
- Passyunk (neighborhood character)

**Environmental Details:**
- Trash cans
- Street signs
- Fire hydrants
- Parking authority (enemy!)
- Other vehicles

### Truck Interior
**Essential Elements:**
- Loading area (spatial puzzle view)
- Driver seat (transition screen)
- Items stacked (packing game visual)

---

## UI Elements

### HUD (Heads-Up Display)
**Elements:**
- Stamina bar (top-left)
- Cash counter (top-right)
- Carried item indicator (near player)
- Job checklist (toggleable)

**Style:**
- Minimal, non-intrusive
- Consistent with game palette
- Clear icons/symbols
- Readable font

### Menus
- Start screen
- Job selection
- Skills/progression screen
- Pause menu
- Save/load
- Game over/fired screen

**Design Notes:**
- Box-based layouts (GBC standard)
- Clear text hierarchy
- Button prompts where needed
- Consistent spacing

---

## Animation Standards

### Character Animation
- **Walk cycle:** 4 frames minimum (can be 2 for slower movement)
- **Idle:** 2-4 frame subtle bob or breath
- **Action:** 2-3 frames (lift, drop, etc.)
- **Framerate:** 8-12 FPS typical for character animation

### Object Animation
- Furniture: Mostly static (save memory)
- Interactive items: Simple 2-frame blink or glow
- Environmental: Minimal (flags, smoke, water)

### Special Effects
- Dust puff (item dropped): 3-4 frames
- Crash/break: 4-5 frames
- Cash register: 2-3 frames
- Sweat drops (strain): 2-frame loop

---

## File Naming Conventions

### Characters
```
Format: char_[name]_[state]_[direction]_[frame].png

Examples:
char_barry_idle_down_01.png
char_barry_walk_left_03.png
char_barry_carry_up_02.png
```

### Furniture
```
Format: furn_[item]_[variant].png

Examples:
furn_couch_brown.png
furn_chair_red.png
furn_box_01.png
```

### Backgrounds
```
Format: bg_[location]_[variant].png

Examples:
bg_apartment_studio.png
bg_street_rowhouse.png
bg_truck_interior.png
```

### UI
```
Format: ui_[element]_[state].png

Examples:
ui_stamina_full.png
ui_button_a.png
ui_icon_cash.png
```

---

## Asset Pipeline

### Creation Workflow
1. **Sketch:** Rough concept at any size
2. **Pixel:** Create at 1x size (actual pixel dimensions)
3. **Palette:** Apply approved color palette
4. **Animate:** Create frames if animated
5. **Export:** PNG with transparency, indexed color
6. **Validate:** Run through asset validation script
7. **Import:** Add to GB Studio project
8. **Test:** View in-game, iterate

### Tools Recommended
- **Aseprite** (pixel art & animation) - Primary
- **GraphicsGale** (alternative)
- **Photoshop/GIMP** (with pixel-perfect settings)
- **GB Studio** (preview and testing)

### Quality Checklist
- [ ] Correct dimensions (8x8, 16x16, etc.)
- [ ] Uses approved palette only
- [ ] Transparent background where appropriate
- [ ] Clear silhouette/readability
- [ ] Consistent style with other assets
- [ ] Proper file naming
- [ ] Optimized file size

---

## Reference Materials

### To Be Collected
- Screenshots of GBC games with similar style
- Photos of Philadelphia locations
- Furniture reference (for accuracy)
- Color palette examples from GBC era
- Pixel art tutorials and technique guides

---

## Evolution of This Guide

This is a living document. As we create assets and discover what works, update this guide with:
- Refined color palettes
- Additional sprite states discovered
- New furniture types needed
- Technical discoveries (what works in GB Studio)
- Style refinements

**Next Steps:**
1. Create Barry sprite concept
2. Create one test furniture item
3. Build one complete room background
4. Test in-game and iterate
5. Update this guide based on learnings

---

**Status:** FOUNDATIONAL DRAFT
**To be expanded:** During Phase 1, Week 3 of development plan
**Owner:** Art department (with Design collaboration)
