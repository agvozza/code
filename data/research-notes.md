# Phase 1 research notes: exercise video database

Checked 2026-10-24. All 26 exercises have a primary and a backup video, and all 52 videos passed the checks below. Every entry in `exercises.json` is marked `verified`; none needed `needs_review`.

## How each video was verified

| Check | How | Result |
| --- | --- | --- |
| Public | The video appears in YouTube's public search results (unlisted and private videos do not) | 52 / 52 |
| Live and embeddable | YouTube oEmbed endpoint returned HTTP 200 (it returns 401 when embedding is disabled and 404 when a video is private or removed) | 52 / 52 |
| Title and channel | Copied exactly from the oEmbed response, including odd spacing | 52 / 52 |
| Shows the exercise | Viewed YouTube's thumbnail plus its three auto-generated stills from about 25%, 50% and 75% of the way through, to confirm the exercise is shown, the camera angle, and who demonstrates it | 52 / 52 |
| Length | Duration from the search listing | 49 of 52 are under 3 minutes; the other 3 are backups, noted below |

**Limits.** The YouTube watch page was rate-limited from the build environment, so I could not read full descriptions, chapter lists or captions, or listen to the audio. Two consequences:

- Every `start` is `0`. Videos were chosen to be short so no timestamp is needed. All 26 primaries are under 3 minutes; the 3 longer videos are backups.
- The coaching talk-over was not heard. The parent review step in the brief still matters: watch each primary once and swap any that are not right.

The coaching `cues` in `exercises.json` are standard cues written for the app (the split-squat cues are the brief's). They are not quotes from the videos.

## Preferred sources from the brief: what happened

| Source | Outcome |
| --- | --- |
| FIFA 11+ (official) | FIFA's channel appears to post one short clip per exercise ("The "11+" Warm-up: Part 1" shows only straight-ahead running; the series runs to "Part 11a"). Used a complete Part I walkthrough from University of Iowa Health Care instead, so one link covers the whole warm-up. |
| The Art of Coaching Volleyball | Chosen for serving (primary). Its approach videos are coaches talking (5–8 min) or middle-hitter specific, so other sources were used for approach footwork. |
| Project Pure Athlete (Tyler Ray, Chase Skinkis) | Tyler Ray's videos now sit on "The Art of Jumping" channel, which links to projectpureathlete.com. Its volleyball approach videos run 5–30 minutes and are talk-heavy; without readable chapters no demo timestamp could be confirmed. Rejected for length. |
| Overtime Athletes (Chris Barnard) | Channel "overtimeathletes" has vertical-jump programme videos (2–10 min) but no single-exercise demos matching this list. Not used. |
| USA Volleyball | Long-form coaching sessions (5–34 min), e.g. "Volleyball FLOAT SERVE Basics" (14:19). No timestamps could be confirmed. Not used. |
| Physical-therapy channels | Used heavily: Children's Hospital Colorado athletic-trainer series, St. Elizabeth Healthcare ACL Injury Prevention Program (teen demonstrators), MGH Orthopaedics, Hinge Health, MedStar Health, East Cheshire NHS Trust, Middlebury College sports medicine. |

## Choices by exercise

Format: chosen primary and backup, then other videos considered and why they were not chosen. Lengths are m:ss.

**fifa-11-warmup**
- Primary: University of Iowa Health Care, "FIFA 11+ Complete Warm-up Program - Part I - Running Exercises" (2:34). Complete Part I in one clip, university sports medicine.
- Backup: Salmon Bay Physical Therapy, "FIFA 11+ Part 1: Warm-Up" (2:00).
- Rejected: FIFA "The "11+" Warm-up: Part 1" (1:05, one exercise only); E3 Rehab full program (11:34), OrthoVirginia (10:33), CHKD (10:13), US Club Soccer (5:14), all too long; E3 Rehab Exercise Library and Ontario Soccer per-exercise clips (would need six links).

**snap-down**
- Primary: PRO+ Sports Medicine Education, "How to Perform a Snap Down for Landing Mechanics" (0:19). Clean front view.
- Backup: basketball.physio, "Introduction to Landings: Snap Downs" (0:31). Female physio; ends with a split-stance variation.
- Rejected: SPARC Physiotherapy double-leg snap down (0:37, good alternate); Train With Cuz (0:32, less established source); PLT4M (1:29, mostly two coaches talking); LPI Physical Therapy (Shorts format, ACL-rehab framing); The Basketball Doctors snap-down series (4:04, too long).

**box-step-down-stick**
- Primary: Forward Physical Therapy LLC, "Double Leg Drop Landing" (0:17). Female PT, low box, front view shows knee alignment.
- Backup: Honest Fitness, "Drop Landing" (0:36). Side view, low box.
- Rejected: St Pete Physical Therapy box drops (0:18, alternate); Strength Coach Nause drop and stick (0:16); Performance Center CPH box drop (0:09, no instruction); McMaster Performance step-off (0:38, old low-resolution video); HSS "ACL Injury Prevention: Jumping and Landing Technique" (2:56, general landing, no box); Science in Dance 20-inch box (labelled advanced); single-leg drop landings (too advanced).

**approach-footwork**
- Primary: Championship Productions, "Develop Your Footwork for a Stronger Attack!" (2:55). University of Louisville head coach Anne Kordes teaching footwork to a line of young female players, no ball.
- Backup: Four Athletes, "How to Four Step Approach in Volleyball" (1:23).
- Rejected: AVCA "Three Step Approach for Young Players" (5:02, excellent youth content but over 3 min and 3-step only); Kristen Dozier-Williams "The Perfect 3 Step Volleyball Approach!" (0:54, female demo with captions, good alternate, smaller source); Art of Coaching Volleyball "Hitting Approach (Portland Clinic)" (5:52, coaches talking), "Teaching hitter footwork on a push set" (2:07) and "Middle hitter transition footwork" (3:26), both middle-specific; Natalie Reagan "4 Step Approaches" (match footage, not a demo); Union Volleyball Academy (2:41, long talking intro); Club V (3:12); TORQVB "Approach Variations" (2:37, talking head).

**approach-jump**
- Primary: TORQVB, "The Approach" (0:51). Side-view breakdown of approach and arm swing.
- Backup: Drees Performance Training, "Approach Jump Technique - How to Perform a Volleyball Approach Jump" (5:25). Over 3 min; sampled frames all show demonstration.
- Rejected: The Art of Jumping (Tyler Ray) "How to Jump Higher on Court and Sand" (5:41), "Almost Perfect Volleyball Approach" (5:11), "Volleyball Approach Keys with an Olympian" (19:24), all long and talk-heavy; Elevate Yourself 3-step breakdown (2:53, vertical format ending in a promo) and 13:51 version; Overtime Athletes vertical-jump videos (no approach demo); TORQVB "The Outside Hitter Approach" (0:23, same channel as primary).

**squat-jump**
- Primary: PhysioplusHG, "Stability: Double Leg Squat Jump & Stick" (0:33). Female athlete, front view.
- Backup: Children's Hospital Colorado, "Exercises with an Athletic Trainer: Double Leg Jumps with Eccentric Landing" (0:59).
- Rejected: Scope Sports Injury (0:27, good alternate); High Performance Content and Robert McLean clips (vertical phone video); several 0:06–0:11 clips with no instruction.

**pogo-hops**
- Primary: Therapeutic EDGE, "Double-Leg Pogo Hops in Place | Ankle & Plyometric Exercise" (1:35). PT clinic.
- Backup: Runna, "Pogo Jumps Tutorial - Proper Form and Technique" (0:28). Female demonstrator.
- Rejected: Movement As Medicine pogo progression (3:28, multi-direction); Therapeutic EDGE multidirectional pogos (more advanced than plan); XIP quickness videos.

**lateral-bound**
- Primary: Littauer Strength Training, "Lateral Bound w/ Stick (Speed Skater)" (0:33).
- Backup: X3 Performance, "Skater Bound with Stick Landing" (0:21). On-screen cues.
- Rejected: Children's Hospital Colorado "Skaters with Floor Touch" (continuous skaters, no stick); Pat Cormier (0:26, alternate); short no-instruction clips.

**bodyweight-squat**
- Primary: Children's Hospital Colorado, "Exercises with an Athletic Trainer: Air Squats" (0:59).
- Backup: St. Elizabeth Healthcare, "ACL Injury Prevention Program: Strengthening - Squats" (1:15). Teen demonstrator.
- Rejected: IU Health "Squat (Bodyweight)" (1:10, good alternate); Cincinnati Children's "Strength Training For Young Athletes" (9:27, general talk); ATHLEAN-X (hype style).

**goblet-squat**
- Primary: National Academy of Sports Medicine (NASM), "How to do a Goblet Squat | Proper Form & Technique" (0:29). Female, front and side views.
- Backup: Denvyr | Tall Girl Nutritionist, "How to do a Goblet Squat // Form & Setup!" (0:48). Female demonstrator.
- Rejected: St. Elizabeth "Squats with Dumbbells" (a dumbbell in each hand, not goblet); BuiltLean (1:06, mostly talking head); Men's Health (0:48, alternate); Jack Hanrahan (11:14, long).

**split-squat**
- Primary: Hinge Health, "How to Do a Split Squat: A Guide from Physical Therapists" (1:03). Female, side view.
- Backup: East Cheshire NHS Trust, "Physiotherapy: Split squat lunge" (0:47). Female, side and front views with written steps.
- Rejected: Get Exercise Confident (3:17, over 3 min); Revival Performance PT (2:17, talking intro); Sussex Community NHS (1:31, alternate); SilverSneakers (2:26, older-adult audience); Atomic Athlete (0:25, loaded with dumbbells); E3 Rehab (12:52, long).

**rfe-split-squat**
- Primary: National Academy of Sports Medicine (NASM), "How to do a Bulgarian Split Squat | Proper Form & Technique" (0:21). Female, side view; holds dumbbells (do it bodyweight or with one light dumbbell).
- Backup: Easthill Physiotherapy & Acupuncture, "Rear Foot Elevated Split Squat (RFESS)" (1:27).
- Rejected: Refinery Athletics (0:33, female, alternate); Get Strong with Emily (1:19, at-home bodyweight, smaller source); ATHLEAN-X (profanity in title); Squat University (4:07); Jack Hanrahan (11:09).

**glute-bridge**
- Primary: Children's Hospital Colorado, "Core Exercise: Bridge" (1:37). Female, side view.
- Backup: St. Elizabeth Healthcare, "ACL Injury Prevention Program: Strengthening - Double Leg Bridge" (1:23). Teen athletes.
- Rejected: Hinge Health (0:54, alternate); Well+Good (2:09); Pamela Reif burnout (10:41, a workout, not a demo).

**single-leg-glute-bridge**
- Primary: MedStar Health, "Strengthening Exercise for ACL: Single Leg Bridge" (0:27). Side view.
- Backup: Middlebury College, "Single Leg Glute Bridge" (0:25). College sports medicine, on-screen cues.
- Rejected: Children's Hospital Colorado "Bridge with Leg Extension" (a different variation); Dr. Carl Baird (2:03, alternate); Well+Good (3:29).

**single-leg-rdl**
- Primary: Children's Hospital Colorado, "Exercises with an Athletic Trainer: Single Leg RDL" (1:21). Bodyweight, for weeks 1–2.
- Backup: OPEX Fitness, "Dumbbell Single Leg Romanian Deadlift - OPEX Exercise Library" (0:19). Dumbbell version for weeks 3–4 (two dumbbells shown; she uses one, in the hand opposite the standing leg).
- Rejected: Girls Gone Strong bodyweight SL RDL (0:27, female, alternate); Squat University (9:17); Catalyst Athletics (weightlifting library).

**calf-raise**
- Primary: MGHOrthopaedics, "Calf Raises" (0:28). Female, side view, chair for balance.
- Backup: St. Elizabeth Healthcare, "ACL Injury Prevention Program: Strengthening - Bilateral Calf Raise" (0:51).
- Rejected: Children's Hospital Colorado "Standing Calf Raises" (1:02, off a step with a dumbbell, harder than the plan); Hammer Strength (machine); Colossus Fitness (2:02).

**plank**
- Primary: Children's Hospital Colorado, "Core Exercise: Plank" (1:06). Female, side view.
- Backup: St. Elizabeth Healthcare, "ACL Injury Prevention Program: Strengthening - Standard Plank" (1:06). Teen demonstrator.
- Rejected: Get Exercise Confident (2:45); Calisthenicmovement "STOP Doing Planks Like That!" (hype style).

**side-plank**
- Primary: Children's Hospital Colorado, "Core Exercise: Side Plank" (1:11). Female, front view.
- Backup: St. Elizabeth Healthcare, "ACL Injury Prevention Program: Strengthening - Side Plank" (1:17). Teen girl and boy.
- Rejected: NASM side plank (0:17, alternate); McGill "Big 3" chiropractic clip.

**shuffle-to-dig**
- Primary: Choose Coaching, "Volleyball Lateral Shuffle Dig" (0:23). The exact drill: shuffle, then dig a coach's toss.
- Backup: SportVideos, "Volleyball Defensive Movement Drills - Coach Ashlie Hain" (3:42). Youth female players; just over 3 min.
- Rejected: MAH Volleyball "No-Beat Footwork Rule" (0:54); Reid Hall agility routine (0:50); Art of Coaching Volleyball dynamic warm-up (1:31, team drill); Natke Volleyball (8:55) and Lexi Rodriguez defensive training (9:35), both long.

**reaction-drill**
- Primary: Volleyball University, "3 Partner Reaction Drills for Defense" (2:29). Partner toss and drop, female athlete.
- Backup: Junior Volleyball Association, "Workout Wednesday: 4 Quick Reaction Drills" (1:09).
- Rejected: Colorado Volleyball Association "Burn Drill" (3:27, team drill); "Tip or Hit - Defensive Reaction" (1:17, needs a net and hitter); Elevate Yourself (12:22) and VolleyCountry (8:10), both long.

**serving**
- Primary: The Art of Coaching Volleyball, "How to float serve in volleyball" (0:54). Young female players, side view.
- Backup: AVCA Volleyball, "AVCA Video Tip of the Week: Mastering the Float Serve" (3:43). Just over 3 min.
- Rejected: USA Volleyball "Volleyball FLOAT SERVE Basics" (14:19, no timestamp); Art of Coaching Volleyball "Serving Tips - Terry Liskevych" (1:42, several serve types) and serving progression drill (4:49); Elevate Yourself (9:54); PMEvolleyball (16:50).

**band-external-rotation**
- Primary: MGHOrthopaedics, "Standing External Rotation with Resistance Band" (0:46). Female, front view, towel roll.
- Backup: Children's Hospital Colorado, "Exercises with an Athletic Trainer: Shoulder Internal and External Rotation with Band" (1:25).
- Rejected: AskDoctorJo seated band ER (0:38, alternate); Onyx PT (0:19); E3 Rehab rotator cuff (12:23, long).

**band-ytw**
- Primary: Children's Hospital Colorado, "Exercises with an Athletic Trainer: Is, Ts, Ys and Ws" (1:53). Prone version, no band; can be done on the floor.
- Backup: Alpha Chiropractic & Physical Therapy, "YTWL Shoulder Exercise (with Resistance Band)" (1:44). Standing band version.
- Parent choice: the id says "band", the primary is the prone no-band version. Swap them if she will do it with the band.
- Rejected: The Active Life prone YTW (0:31); TRedTraining standing band YTW (0:27, unknown source); Gotham PT (3:14, filmed from behind).

**band-scap-retraction**
- Primary: Hinge Health, "How to Do Band Pull Aparts: A Guide from Physical Therapists" (1:12). Female, front view.
- Backup: The Active Life, "Band Pull Apart" (0:23). PT clinic.
- Rejected: Tangelo chiropractor (0:51); Physical Therapy 101 series (2:56); Conor Harris "STOP Doing Banded Pull-Aparts" (8:14, hype); joedefranco (3:59).

**swim-kick-set**
- Primary: Speedo, "Front Crawl Swimming Drills | Kickboard" (1:22). Female swimmer, underwater views.
- Backup: Coach Robb Beams, "Coach Robb: Swimming: How To Use a Kickboard" (2:47). On-screen technique captions.
- Rejected: MySwimPro kickboard tips (0:35, about why, not how); Rocket Swimming (5:05); Global Triathlon Network kick drills (7:00).

**backstroke**
- Primary: Speedo, "Backstroke Swimming Technique | Stroke" (1:54).
- Backup: SIKANA English, "Swimming: Basic Technique | Backstroke" (2:28).
- Rejected: Olympic Games "How to master Backstroke Swimming" (2:52, focuses on the kick, mostly talk); U.S. Masters Swimming body position (2:35, alternate); Global Triathlon Network (3:52, 5:01); MySwimPro 30-second animation.

## Videos over 3 minutes

All three are backups and start at 0: approach-jump (5:25), shuffle-to-dig (3:42), serving (3:43). None of the primaries is over 3 minutes.
