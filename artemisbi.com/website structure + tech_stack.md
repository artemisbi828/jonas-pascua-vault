| **Tool**          | **Formal Definition**                                                               | **The Analogy**                                                                                                                                                                    | **Why for this build?**                                                                                                 |
| ----------------- | ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **Vite**          | A modern build tool that serves code via native browser modules during development. | **The Formula 1 Pit Crew.** Instead of rebuilding the entire car every time you change a tire (like older tools), they swap just the tire while the car is moving.                 | It provides near-instant feedback when you tweak your UX copy or layout.                                                |
| **React**         | A library for building user interfaces using isolated, reusable components.         | **LEGO Sets.** You build a "Button" brick and a "Hero" brick once, then snap them together wherever you need them.                                                                 | Keeps the UI modular. If you change your global "Button" style, it updates everywhere.                                  |
| **TypeScript**    | A superset of JavaScript that adds static "types" (definitions) to your data.       | **The Blueprint & Inspector.** It checks that your "Hero" component is actually receiving "Text" and not a "Number" before you even try to run the code.                           | Prevents "broken" states. If a piece of content is missing, the code won't compile, saving you from a broken live site. |
| **Tailwind CSS**  | A utility-first CSS framework that uses predefined classes in HTML.                 | **The Professional Painter’s Palette.** Instead of mixing your own "Blue-ish" paint from scratch every time, you have a set of labeled, consistent colors and brushes ready to go. | Perfect for the "HiHello" look. It forces you to use consistent spacing and colors without a massive CSS file.          |
| **Nginx**         | A high-performance web server and reverse proxy.                                    | **The Maître D’ of a restaurant.** It stands at the door of your Linux VM, takes the customer's request, and serves them the correct static file (your website) instantly.         | It is the most robust way to serve a static site on Linux. It handles high traffic with almost zero CPU usage.          |
| **Framer Motion** | A production-ready motion library for React.                                        | **The Puppeteer.** It tells your React components exactly how to glide, fade, or spring into place.                                                                                | This is how you achieve the "premium" feel of hihello.com—subtle, smooth entrance animations.                           |

# Solid/Dry Structure
my-portfolio/
├── public/              # Raw static assets (favicon, robots.txt)
├── src/
│   ├── assets/          # Images and SVGs used in components
│   ├── components/      # REUSABLE UI units (The "LEGO" bricks)
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   └── Navbar.tsx
│   ├── content/         # YOUR TALKING POINTS (The "Copy" data)
│   │   ├── copy.ts      # The single source of truth for text
│   │   └── projects.ts  # Data for your UX case studies
│   ├── sections/        # PAGE-SPECIFIC LAYOUTS
│   │   ├── Hero.tsx     # Uses copy.ts to fill content
│   │   └── ProjectGrid.tsx
│   ├── styles/          # Global CSS & Tailwind config
│   │   └── index.css
│   ├── App.tsx          # The "Master Assembly" file
│   └── main.tsx         # The entry point for the browser
├── .gitignore           # Files to exclude from GitHub
├── tailwind.config.js   # Design tokens (Colors, Fonts)
├── tsconfig.json        # TypeScript rules
└── vite.config.ts       # Vite configuration

