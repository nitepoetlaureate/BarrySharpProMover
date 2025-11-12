# Barry Sharp's Pro Mover - GB Studio Code Patterns & Standards

**Version:** 1.0
**Date:** November 12, 2025
**Status:** DRAFT - To be expanded during development

---

## GB Studio Overview

### What is GB Studio?
- Visual game development tool for Game Boy/Game Boy Color
- Drag-and-drop interface with scripting system
- Exports to authentic ROM files
- Limited programming via event system and custom engine modifications

### Version
- Target: GB Studio 3.x or latest stable
- Engine: GBDK-based
- Export: Game Boy Color (.gbc) ROM format

---

## Project Structure

### GB Studio Project File
```
BARRY-SHARP-PRO-MOVER-1.gbsproj
```

### Expected Organization
```
Project Root/
├── assets/              (All game assets)
│   ├── backgrounds/    (160x144 PNG files)
│   ├── sprites/        (Sprite PNGs)
│   ├── music/          (MOD/UGE files)
│   └── sounds/         (Sound effects)
├── scenes/             (GB Studio scenes - defined in .gbsproj)
├── scripts/            (Custom GBDK code if needed)
└── build/              (Output directory)
```

---

## GB Studio Event System

### Core Concepts

**Actors:** Sprites that can move, animate, interact
**Triggers:** Invisible zones that activate scripts when player enters
**Events:** Visual scripting blocks that define game logic
**Variables:** Global and local storage for game state
**Scenes:** Individual screens/rooms in the game

### Event Categories

**Movement:**
- `Actor Move` - Move actor to position
- `Actor Set Direction` - Face specific direction
- `Actor Animate` - Play animation
- `Camera Move` - Pan camera

**Logic:**
- `If Variable Compare` - Conditional logic
- `Variable Set` - Assign values
- `Math` - Arithmetic operations
- `Random` - Generate random numbers

**Dialogue:**
- `Text Display` - Show dialogue box
- `Choice` - Player decision branching
- `Text Set Animation Speed` - Control text appearance

**Audio:**
- `Music Play` - Start background music
- `Music Stop` - Stop music
- `Sound Play` - Play sound effect

**Scene:**
- `Switch Scene` - Load new scene
- `Scene Push State` - Save current scene state
- `Scene Pop State` - Return to saved scene

---

## Variable Management

### Global Variables (Max 512)
Use organized naming convention:

**Player Stats (0-49):**
```
00: player_stamina_current
01: player_stamina_max
02: player_strength
03: player_speed
04: player_cash
05: player_job_completed_count
...
```

**Job State (50-99):**
```
50: job_current_id
51: job_items_remaining
52: job_time_remaining
53: job_difficulty
54: job_payment
...
```

**Relationship/Story (100-149):**
```
100: rel_coworker_1
101: rel_coworker_2
102: rel_coworker_3
103: story_day_number
104: story_fires_count
105: story_ng_plus_level
...
```

**Carried Item State (150-179):**
```
150: carried_item_id
151: carried_item_weight
152: carried_item_fragile
...
```

**Flags/Booleans (180-229):**
```
180: flag_tutorial_complete
181: flag_can_use_stairs
182: flag_truck_unlocked
183: flag_job_1_done
...
```

**Temporary/Scratch (230-255):**
```
230-255: temp_1, temp_2, etc.
Use for calculations, loops, temporary storage
```

### Local Variables (Per-Scene)
- Use for scene-specific temporary state
- Reset when scene changes
- Examples: NPC dialogue state, item positions

---

## Common Patterns

### Pattern: Carrying Mechanic

**Pickup Item:**
```
Event: Player Interacts with Furniture

1. If Variable Compare: carried_item_id == 0 (not carrying)
   - If Variable Compare: player_strength >= item_weight
     - Variable Set: carried_item_id = [this item]
     - Variable Set: carried_item_weight = [weight]
     - Actor Set Sprite: player -> carrying sprite
     - Actor Hide: this_furniture
     - Sound Play: pickup_sound
   - Else (too heavy)
     - Text Display: "Too heavy!"
     - Actor Animate: player -> strain animation
2. Else (already carrying)
   - Text Display: "I'm already carrying something!"
```

**Drop Item:**
```
Event: Player Presses B Button

1. If Variable Compare: carried_item_id != 0
   - Actor Set Position: spawn furniture at player position
   - Actor Show: furniture_[carried_item_id]
   - Variable Set: carried_item_id = 0
   - Actor Set Sprite: player -> normal sprite
   - Sound Play: drop_sound
   - If Variable Compare: carried_item_fragile == 1
     - If [check if on stairs or dropped from height]
       - Sound Play: crash_sound
       - Text Display: "Oh no! It broke!"
       - Variable Math: player_cash -= 50
```

### Pattern: Stamina System

**Stamina Drain While Carrying:**
```
Event: Custom Event (called every N frames)

1. If Variable Compare: carried_item_id != 0
   - Variable Math: player_stamina_current -= carried_item_weight
   - If Variable Compare: player_stamina_current <= 0
     - Variable Set: player_stamina_current = 0
     - Call Event: force_drop_item
     - Actor Animate: player -> exhausted
     - Text Display: "Too tired..."
```

**Stamina Regeneration:**
```
Event: Custom Event (called when resting)

1. If Variable Compare: carried_item_id == 0
   - If Variable Compare: player_stamina_current < player_stamina_max
     - Variable Math: player_stamina_current += 2
```

### Pattern: Job Structure

**Job Start:**
```
Event: Hub -> Job Selected

1. Variable Set: job_current_id = [selected job]
2. Variable Set: job_items_remaining = [total items]
3. Variable Set: job_time_remaining = [time limit]
4. Scene Switch: job_[id]_scene
5. Music Play: job_theme
6. Text Display: [job briefing]
```

**Item Loaded in Truck:**
```
Event: Player Enters Truck Trigger While Carrying

1. If Variable Compare: carried_item_id != 0
   - Variable Math: job_items_remaining -= 1
   - Variable Math: player_cash += [item value]
   - Variable Set: carried_item_id = 0
   - Actor Set Sprite: player -> normal
   - Sound Play: cash_register
   - If Variable Compare: job_items_remaining == 0
     - Call Event: job_complete
```

**Job Complete:**
```
Event: All Items Loaded

1. Music Stop
2. Music Play: success_jingle
3. Text Display: "Job complete! Earned $[payment]"
4. Variable Math: player_cash += job_payment
5. Variable Math: player_job_completed_count += 1
6. Variable Math: rel_coworkers += 5 (if coworker present)
7. Wait: 2 seconds
8. Scene Switch: hub_scene
```

### Pattern: Dialogue System

**Simple NPC Dialogue:**
```
Event: Player Interacts with NPC

1. Actor Set Direction: npc -> face player
2. Text Display: [dialogue line 1]
3. Text Display: [dialogue line 2]
4. Actor Set Direction: npc -> original direction
```

**Choice-Based Dialogue:**
```
Event: Player Interacts with Important NPC

1. Text Display: "Want to hear about [topic]?"
2. Choice:
   - "Yes" -> Call Event: explain_topic
   - "No" -> Text Display: "Okay, later."
3. Variable Set: flag_npc_talked = 1
```

### Pattern: Day/Time System

**Advance Day:**
```
Event: End of Job / Sleep

1. Variable Math: story_day_number += 1
2. Call Event: check_fires_risk
3. If Variable Compare: story_day_number MOD 7 == 0
   - Call Event: party_night
4. Scene Switch: morning_hub
```

---

## Performance Considerations

### GB Studio Limits

**Sprites:**
- Max 40 sprites on screen
- Max 10 per horizontal line
- Use sparingly, hide when not needed

**Tiles:**
- Max 192 unique background tiles per scene
- Reuse tiles across scenes
- Use palette swaps for variety

**Events:**
- Keep event chains reasonably short
- Use custom events to organize complex logic
- Avoid deep nesting (performance impact)

**Variables:**
- 512 global max - plan usage carefully
- Local variables are free but reset
- Use flags (0/1) for booleans to save space

### Optimization Tips

1. **Reduce Active Sprites:**
   - Hide sprites when off-screen
   - Use triggers to spawn/despawn dynamically

2. **Simplify Event Logic:**
   - Break complex events into smaller custom events
   - Avoid unnecessary variable checks
   - Use local variables when possible

3. **Manage Music/Sound:**
   - Keep music file sizes reasonable
   - Limit simultaneous sound effects
   - Reuse sound effects where possible

4. **Scene Design:**
   - Keep scenes focused (single room/area)
   - Use scene transitions strategically
   - Preload critical scenes

---

## Custom Engine Code (If Needed)

### When to Use Custom Code
- Complex math beyond event system
- Custom movement physics
- Advanced collision detection
- Performance-critical functions

### Integration with GB Studio
- GB Studio allows custom engine plugins
- Write in C using GBDK
- Build custom events that call C functions
- **Caution:** Advanced technique, use sparingly

### Example Use Cases
- Precise item physics (rotation, bouncing)
- Advanced AI pathfinding
- Custom rendering effects
- Optimized collision systems

---

## Testing & Debugging

### GB Studio Debugging
- Use "Play" mode to test quickly
- Use "Build Web" for browser testing
- Use "Build ROM" + emulator for authentic testing
- Check sprite limits with debug overlays

### Common Issues

**Sprite Flicker:**
- Too many sprites on one scanline
- Solution: Reduce sprites or offset Y positions

**Slow Performance:**
- Too many active events
- Solution: Optimize event logic, reduce complexity

**Variable Conflicts:**
- Multiple systems using same variables
- Solution: Follow variable organization plan strictly

**Scene Transitions Broken:**
- Incorrect scene IDs or positions
- Solution: Double-check scene connections

---

## Code Style Guidelines

### Event Naming
- Use descriptive names: `job_complete`, not `event_1`
- Prefix by category: `player_`, `job_`, `npc_`, `system_`
- Use snake_case consistently

### Custom Event Organization
```
System Events:
- system_init
- system_update_hud
- system_save_game

Player Events:
- player_pickup_item
- player_drop_item
- player_use_stairs

Job Events:
- job_start
- job_item_loaded
- job_complete
- job_failed
```

### Comments in Events
- GB Studio allows text notes in events
- Use to explain complex logic
- Document variable usage
- Mark TODOs and FIXMEs

---

## Integration with Automation

### LangFlow Code Department
- Can generate event sequences based on design specs
- Can validate event logic against standards
- Can suggest optimizations
- Can check variable usage conflicts

### Asset Integration
- Code events reference asset filenames
- Follow asset naming conventions strictly
- Automation can validate asset references

---

## Next Steps

1. **Map out all scenes** needed for vertical slice
2. **Define all variables** using organization system above
3. **Create custom events** for core mechanics
4. **Implement first job** as proof of concept
5. **Test thoroughly** and document learnings
6. **Update this guide** based on discoveries

---

## Resources

### GB Studio Documentation
- Official docs: gbstudio.dev/docs
- Community forum: gbstudio.dev/community
- Example projects: GitHub GB Studio repos

### GBDK Resources (for custom code)
- GBDK documentation
- Game Boy programming manual
- Pan Docs (complete GB hardware specs)

### Learning Materials
- GB Studio tutorial videos (YouTube)
- Game Boy dev tutorials
- Pixel art and retro game design resources

---

**Status:** FOUNDATIONAL DRAFT
**To be expanded:** As we implement mechanics and discover patterns
**Owner:** Code department (with input from all departments)
