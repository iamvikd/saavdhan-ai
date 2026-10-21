# Prompts used to build Saavdhan

Copy any prompt below into an AI assistant (Claude, ChatGPT, Gemini). Each one returns a working file. Save the reply as `index.html` and double-click it.

## 1. The master prompt (rebuilds the whole toolkit)

```
Build a single-file HTML web app called "Saavdhan" for a disaster resilience
event in India, for students from many states. Theme: "From Awareness to Action".
It must work offline, with all CSS and JavaScript inside the file, and be
mobile friendly. Use tabs for these modules:

1. Why this matters: India's national hazard figures and a 2025 Punjab flood
   case study (I will give you the numbers and sources; do not invent any).
   Add a "My State" picker listing each state's main hazards, and a tab that
   explains Google Flood Hub's severity levels with a gauge-to-action simulator.
2. Alert to Action: user picks a hazard (flood, heatwave, earthquake) and a
   language (English, Hindi and the main regional languages). Show 5 to 6 short action steps, with a
   "Read aloud" button using the browser's speech feature.
3. Household flood risk estimator: 7 dropdown questions, a score out of 17,
   a coloured meter, advice for each level, and a table explaining every
   point that was added. Say clearly that it is a teaching model.
4. Family emergency plan: a form that generates a printable one-page plan.
5. Go-bag checklist with a progress bar saved in localStorage.
6. Post-flood waste guide: tap an item to see its waste stream, safe
   handling steps and what to avoid.
7. Idea Lab: cards listing gaps in public disaster tools, plus a table on
   moving from prototype to hackathon, incubator and seed funding.

Include emergency numbers 112, 108 and 101. Add a footer saying it is an
educational demo, not an official warning system.
```

## 2. Live demo prompts (each takes about one minute)

Use these on stage to show the audience that a working tool can be made in front of them.

**A. Heatwave buddy check**
```
Make a single HTML file: a "Heatwave Buddy Check" app for elderly people.
One big green button "I am OK today". It records the time. If the button
has not been pressed by 11 am, show a red banner "Call your buddy" with a
phone number field. Large fonts, Hindi and English labels, works offline.
```

**B. Relief camp counter**
```
Make a single HTML file for a flood relief camp volunteer. Inputs: number
of adults, children, elderly and infants. Output: a daily supply list
(water litres, meals, ORS packets, diapers, blankets) using clear
assumptions shown on screen, and a button to copy the list for WhatsApp.
```

**C. Waste sorting quiz**
```
Make a single HTML file: a 6 question quiz on sorting post-flood waste
(wet, dry, hazardous, e-waste, biomedical, construction debris). Show the
correct answer and a one-line reason after each question, and a score at
the end. Bright colours, mobile friendly.
```

## 3. Rules that keep AI output trustworthy

- Give the AI your numbers and sources. Tell it not to invent data.
- Ask it to show assumptions on screen.
- Check translations with a native speaker.
- Test with five real users before calling it finished.
