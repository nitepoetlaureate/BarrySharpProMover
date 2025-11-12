# Barry Sharp's Pro Mover - Music & Audio Direction

**Version:** 1.0
**Date:** November 12, 2025
**Status:** DRAFT - To be expanded during audio production

---

## Technical Constraints

### Game Boy Color Audio Hardware

**Sound Channels:**
- **Channel 1:** Square wave (pulse) with sweep
- **Channel 2:** Square wave (pulse) without sweep
- **Channel 3:** Wavetable (custom waveforms)
- **Channel 4:** Noise (percussion/effects)

**Limitations:**
- 4 channels total (monophonic per channel)
- Limited sample quality
- No true stereo (left/right panning only)
- File size constraints

### GB Studio Music Formats
- **Primary:** UGE (GB Studio Music Editor format)
- **Alternative:** MOD files (converted)
- **Recommended Tool:** hUGETracker or GB Studio Music Editor

---

## Musical Direction

### Overall Sound Aesthetic

**Inspirations:**
- Pokemon Crystal soundtrack (nostalgic, melodic)
- Wario Land 3 (quirky, energetic)
- The Legend of Zelda: Oracle series (adventure feel)
- Chiptune artists: Chipzel, Anamanaguchi
- Philadelphia music scene (soul, punk energy)

**Goals:**
- **Memorable:** Catchy melodies that stick
- **Emotionally Resonant:** Support story and character moments
- **Authentic 8-bit:** Embrace GBC sound, don't fight it
- **Dynamic:** Music reflects gameplay state
- **Philadelphia Soul:** Incorporate Philly musical heritage where appropriate

---

## Music Track List

### Main Themes

**1. Title Screen Theme**
- **Mood:** Hopeful, inviting, nostalgic
- **Tempo:** Medium (120-130 BPM)
- **Key:** Major key (C or G major)
- **Length:** 1:00 loop
- **Function:** First impression, sets tone
- **Reference:** Pokemon title themes

**2. Hub/Menu Music**
- **Mood:** Relaxed, contemplative, warm
- **Tempo:** Slow-medium (90-110 BPM)
- **Length:** 1:30 loop
- **Function:** Base between jobs, character moments
- **Reference:** Stardew Valley "A Glimpse of the Past"

**3. Main Job Theme**
- **Mood:** Determined, working, rhythmic
- **Tempo:** Medium-fast (140-150 BPM)
- **Key:** Minor key for challenge
- **Length:** 2:00 loop
- **Function:** Standard moving job music
- **Reference:** Tetris theme A (that driving feel)

### Situation-Specific

**4. Tutorial Job**
- **Mood:** Encouraging, simple, friendly
- **Tempo:** Medium (120 BPM)
- **Complexity:** Simple melody, easy to ignore or focus on
- **Function:** Non-distracting during learning

**5. Time Pressure Job**
- **Mood:** Urgent, stressful (but not panicky)
- **Tempo:** Fast (160+ BPM)
- **Function:** Communicate urgency
- **Variation:** Speed up as time runs low

**6. Night Job**
- **Mood:** Mysterious, lonely, atmospheric
- **Tempo:** Medium-slow (100-120 BPM)
- **Function:** Different time of day feel
- **Use:** Evening/night jobs, special situations

**7. Party Time**
- **Mood:** Celebration, joy, friendship
- **Tempo:** Upbeat (140-160 BPM)
- **Key:** Major, bright
- **Function:** Social moments, victories
- **Philadelphia flavor:** Could incorporate Philly soul influences

### Character Themes (Optional/Advanced)

**8. T-Bone's Theme**
- **Mood:** Gruff but warm, veteran energy
- **Instrumentation:** Strong bass line, steady rhythm
- **Use:** T-Bone-focused moments

**9. DJ's Theme**
- **Mood:** Energetic, chaotic fun
- **Instrumentation:** Fast arpeggios, jumping melody
- **Use:** DJ party events

**10. Maya's Theme**
- **Mood:** Precise, thoughtful, technical
- **Instrumentation:** Clean patterns, mathematical feel
- **Use:** Maya teaching moments

### Emotional Moments

**11. Reflection/Sad Theme**
- **Mood:** Melancholy, nostalgic
- **Tempo:** Slow (70-90 BPM)
- **Key:** Minor
- **Function:** Story moments, losses, endings
- **Reference:** Pokemon "Lavender Town" (less creepy)

**12. Victory Jingle**
- **Mood:** Triumph!
- **Length:** 5-10 seconds
- **Function:** Job complete
- **Reference:** Classic "level complete" stings

**13. Game Over Music**
- **Mood:** Disappointed but not punishing
- **Length:** 15-20 seconds
- **Function:** Getting fired, failure
- **Note:** Should motivate retry, not discourage

### Ambient/Special

**14. Philadelphia Streets Ambient**
- **Mood:** Urban, alive, authentic
- **Style:** Minimal melody, rhythmic
- **Function:** Driving/navigation scenes
- **Could include:** City sounds in rhythm

**15. Truck Interior**
- **Mood:** Contained, focused, puzzle-solving
- **Tempo:** Medium, steady
- **Function:** Packing minigame
- **Reference:** Puzzle game music

**16. End Credits**
- **Mood:** Bittersweet, proud, complete
- **Tempo:** Medium-slow
- **Length:** 2:00+
- **Function:** Roll credits, final emotions
- **Should:** Reprise main theme, bring journey full circle

---

## Sound Effects List

### Player Actions

**Movement:**
- footstep_normal (2-3 variations)
- footstep_heavy (carrying)
- footstep_stairs
- door_open
- door_close

**Carrying:**
- pickup_light
- pickup_medium
- pickup_heavy
- pickup_fail (too heavy)
- drop_soft
- drop_hard
- crash_break (fragile item)

**Effort:**
- grunt_strain_01
- grunt_strain_02
- exhale_tired
- gasp_surprise

### Items/Objects

**Furniture:**
- furniture_slide
- furniture_bump
- furniture_crash
- glass_break
- wood_creak

**Truck:**
- truck_door_open
- truck_door_close
- truck_engine_start
- truck_driving (if needed)

### UI/System

**Interface:**
- menu_select
- menu_back
- menu_confirm
- menu_error

**Feedback:**
- cash_register
- coin_collect
- job_complete
- job_failed
- level_up (skill increase)
- new_item_unlocked

### Environmental

**Locations:**
- doorbell
- phone_ring
- elevator_ding
- elevator_moving
- city_ambience (if used)

**Weather:**
- rain_light
- rain_heavy
- thunder (dramatic moments)

### Social

**NPCs:**
- npc_voice_high (3-4 variations)
- npc_voice_medium
- npc_voice_low
- npc_laugh
- npc_angry
- npc_sad

### Special

**Story Moments:**
- dramatic_sting
- revelation_sound
- transition_whoosh
- time_passing
- ng_plus_start (special)

---

## Audio Design Philosophy

### Clarity First
- Every sound must be distinguishable
- Critical feedback (crash, cash) must be unmistakable
- Never confuse player with unclear audio

### Personality Through Sound
- Sounds should have character
- Barry's grunts should feel earnest
- T-Bone's voice blip should feel gruff
- Environmental sounds should evoke Philadelphia

### Memory Consideration
- GBC has limited audio memory
- Reuse sounds when possible
- Variations through pitch/speed changes
- Prioritize critical sounds

### Dynamic Audio
- Music should react to game state
- Tension increases = music intensity increases
- Success = musical payoff
- Failure = musical sympathy

---

## Implementation Strategy

### Phase 1: Core Audio (Weeks 5-6)
**Priority: HIGH - Needed for basic gameplay**

1. **Essential Music:**
   - Main job theme
   - Hub music
   - Victory jingle

2. **Critical Sound Effects:**
   - Pickup/drop sounds
   - Cash register
   - Menu navigation
   - Footsteps

3. **Test Integration:**
   - Implement in GB Studio
   - Test loop points
   - Verify file sizes
   - Ensure smooth transitions

### Phase 2: Full Music Suite (Weeks 7-8)
**Priority: MEDIUM - Adds variety and depth**

1. **Additional Music:**
   - Time pressure variant
   - Party theme
   - Sad/reflection theme
   - Title screen

2. **Music System:**
   - Dynamic music switching
   - Smooth transitions
   - Situational triggers

### Phase 3: Complete SFX Library (Weeks 9-10)
**Priority: MEDIUM - Polish and juice**

1. **All Remaining Sound Effects**
2. **Variations and Polish**
3. **Environmental Audio**
4. **Character Voice Blips**

### Phase 4: Polish & Mix (Weeks 11-12)
**Priority: LOW - Final quality pass**

1. **Balance all audio levels**
2. **Fine-tune music loops**
3. **Add subtle details**
4. **Final testing on hardware**

---

## Music Composition Guidelines

### Melody Writing

**Keep It Simple:**
- GBC has 4 channels total
- Melody usually on Channel 1 or 2
- Leave room for harmony and bass

**Make It Catchy:**
- Strong hook in first 4-8 bars
- Repetition with variation
- Singable/hummable

**Emotional Arc:**
- Intro establishes mood
- Development section varies theme
- Return to main theme for satisfaction

### Harmony and Bass

**Bass Line:**
- Channel 3 (wavetable) often best for bass
- Strong, simple root notes
- Drives rhythm
- Philadelphia soul: Walking bass lines where appropriate

**Harmony:**
- Channel 2 usually harmony/counter-melody
- Support melody, don't compete
- Create interest in quiet moments
- Fill space when melody rests

### Percussion

**Channel 4 (Noise):**
- Limited to noise-based sounds
- Kick, snare, hi-hat patterns
- Keep simple but effective
- Drives energy

**Patterns:**
- Steady beats for working music
- Syncopation for excitement
- Silence for dramatic effect

### Loop Points

**Critical for GB Music:**
- Must loop seamlessly
- Typically 16, 32, or 64 bars
- Intro can be non-looping
- Test loop points extensively

---

## Sound Design Guidelines

### Creating Effective SFX

**Character Through Constraints:**
- 8-bit sounds can be expressive
- Exaggeration is your friend
- Personality in imperfection

**Functional First:**
- Player must understand what happened
- Sound = feedback
- Test with sound off, then with sound

**Layering (If Possible):**
- Combine multiple short sounds
- Create more complex effects
- Mind the channel limits

### Voice Blips

**For Character Dialogue:**
- Short, pitched noise sounds
- Each character has unique frequency range
- Plays with text appearance
- Examples:
  - Barry: Medium pitch, steady
  - T-Bone: Low pitch, gruff
  - DJ: High pitch, fast
  - Maya: Medium-high, precise

---

## Tools & Workflow

### Recommended Tools

**Music Composition:**
- **hUGETracker** (Free, excellent for GB music)
- **GB Studio Music Editor** (Built-in)
- **FamiTracker** (Alternative, more features)
- **Beepbox** (Online, quick sketches)

**Sound Effects:**
- **Bfxr** (Browser-based, retro SFX)
- **Audacity** (Audio editing)
- **GB Studio SFX tool** (Built-in)
- **ChipTone** (Chiptune SFX generator)

**Testing:**
- **GB Studio** (Preview in context)
- **Emulators** (BGB, mGBA)
- **Real hardware** (Final test if possible)

### Workflow

1. **Sketch:** Hum/sing melody, record ideas
2. **Compose:** Use tracker to create music
3. **Export:** UGE format for GB Studio
4. **Import:** Add to GB Studio project
5. **Implement:** Trigger in scenes/events
6. **Test:** Play and listen in context
7. **Iterate:** Refine based on feel

---

## Music Theory Basics (For Non-Musicians)

### Helpful Concepts

**Tempo (BPM):**
- Slow: 60-90 (sad, contemplative)
- Medium: 100-130 (neutral, working)
- Fast: 140-180 (energetic, urgent)

**Key Signatures:**
- Major keys: Happy, bright, triumphant
- Minor keys: Sad, serious, dramatic
- Common choices: C major, G major, A minor, D minor

**Rhythm:**
- 4/4 time: Standard, "walking" feel
- 3/4 time: Waltz, flowing
- Dotted rhythms: Energy, urgency

### Learning Resources
- YouTube: "How to use hUGETracker"
- Tutorial: "GB Studio music basics"
- Study: Existing GBC game soundtracks
- Practice: Remake simple songs in tracker

---

## Philadelphia Musical Influences

### Incorporating Philly Sound

**Soul/R&B:**
- Strong bass lines
- Call and response patterns
- Emotional delivery
- Groove-based rhythms

**Punk/DIY:**
- Raw energy
- Simple but effective
- Authentic over polished
- Direct emotional expression

**Jazz:**
- Improvisation feel (within loops)
- Complex harmonies (where channels allow)
- Swing rhythms (subtle)

**How to Adapt to GBC:**
- Can't replicate fully, but can evoke
- Rhythmic patterns suggest genres
- Melody contours hint at influences
- Energy and attitude over authenticity

---

## Audio QA Checklist

### Before Finalizing Each Track

**Music:**
- [ ] Loops seamlessly
- [ ] Appropriate tempo and mood
- [ ] Doesn't fatigue listener
- [ ] File size acceptable
- [ ] No audio glitches
- [ ] Tested in GB Studio
- [ ] Tested on emulator
- [ ] Tested in context (during gameplay)

**Sound Effects:**
- [ ] Clear and recognizable
- [ ] Appropriate volume
- [ ] Doesn't clip/distort
- [ ] Matches action timing
- [ ] Variations (if applicable)
- [ ] Tested in multiple contexts

**Integration:**
- [ ] Triggers at correct time
- [ ] Doesn't conflict with other sounds
- [ ] Enhances gameplay, doesn't distract
- [ ] Accessible (not essential for deaf/HoH players)

---

## Accessibility Considerations

### Audio is Enhancement, Not Requirement

**Design Principles:**
- Never require audio to play the game
- Visual feedback for all audio cues
- Subtitles/text for all important information
- Option to disable music/SFX separately (if GB Studio allows)

**Visual Equivalents:**
- Cash register sound → Visual "+$50"
- Crash sound → Screen shake + broken item sprite
- Time warning → Flashing UI element
- Music tempo change → Visual indicator

---

## Next Steps

### Immediate (Weeks 1-4)
1. **Learn hUGETracker** (or chosen tool)
2. **Compose one test track** (main job theme)
3. **Create basic SFX set** (pickup, drop, cash)
4. **Test in GB Studio** (integration workflow)

### Short-term (Weeks 5-8)
1. **Complete Phase 1 audio** (core music and SFX)
2. **Implement in vertical slice**
3. **Playtest with audio**
4. **Iterate based on feedback**

### Long-term (Weeks 9-16)
1. **Complete full soundtrack**
2. **Polish and mix**
3. **Create variations and alternatives**
4. **Final QA pass**

---

## Collaboration with Other Departments

### With Design:
- Music supports intended emotional beats
- Audio reinforces game feel
- Pacing aligns with gameplay rhythm

### With Code:
- Trigger points for music changes
- Dynamic audio implementation
- Memory and performance budgets

### With Art:
- Audio complements visual style
- Thematic consistency
- Timing (animation + sound sync)

---

## Inspiration Playlist

### GBC Soundtracks to Study:
- Pokemon Crystal
- The Legend of Zelda: Oracle of Ages/Seasons
- Wario Land 3
- Dragon Quest Monsters
- Metal Gear Solid (GBC)

### Modern Chiptune Artists:
- Chipzel
- Anamanaguchi
- Disasterpeace
- Jake Kaufman
- Danimal Cannon

### Philadelphia Music:
- The Roots
- Hall & Oates
- Boyz II Men
- Classic Philly soul compilations
- Local Philly punk bands

---

**Status:** FOUNDATIONAL DRAFT
**To be expanded:** During audio production and playtesting
**Owner:** Music/Audio lead (with feedback from all departments)
