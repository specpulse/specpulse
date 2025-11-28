# SpecPulse v2.7.1 Website

🚀 **Modern, responsive landing page for SpecPulse v2.7.1 - The Ultimate AI-Powered Development Framework**

Built with cutting-edge technologies:

- **Tailwind CSS 3.x** - Utility-first CSS framework
- **Alpine.js 3.x** - Lightweight JavaScript framework
- **Custom CSS & JavaScript** - Enhanced animations and interactions
- **shadcn-inspired** - Beautiful, accessible UI components

## Features

✨ **Modern Design**
- Clean, professional landing page for v2.6.9
- Gradient accents and smooth animations
- Mobile-responsive layout
- Dark mode support

🎨 **UI Components**
- **Hero Section**: Eye-catching intro with AI platform showcase
- **8 AI Platform Cards**: Claude, Gemini, GPT, Windsurf, Cursor, OpenCode, Crush, Qwen
- **Interactive Features**: Hover effects, floating particles, typing animations
- **Live Statistics**: 8 AI platforms, 86 commands, 15 bug fixes, 10x productivity
- **Code Examples**: Terminal-style command demonstrations
- **Enhanced Navigation**: Mobile-friendly with smooth transitions
- **Getting Started Guide**: Step-by-step setup instructions

⚡ **Performance**
- Static HTML (no build step required)
- CDN-hosted dependencies (Tailwind CSS, Alpine.js, Google Fonts)
- Optimized animations with GPU acceleration
- Fast load times (< 2s on 3G)
- SEO-friendly with structured data

🎯 **v2.7.1 Highlights**
- **NEW**: Selective AI tool initialization - only create directories for selected AI platforms
- **ENHANCED**: Cleaner project structure with no unnecessary AI directories
- **IMPROVED**: Faster initialization with selective tool loading
- **OPTIMIZED**: Better resource usage by loading only required AI commands
- **MAINTAINED**: All 8 AI platforms working perfectly with selective initialization

🎯 **Previous v2.6.9 Features**
- **NEW**: OpenCode AI integration (featured)
- **ENHANCED**: All 8 AI platforms working perfectly
- **FIXED**: 15 critical bugs and security issues
- **IMPROVED**: Interactive CLI with Ctrl+C support
- **OPTIMIZED**: 86 custom commands across all platforms

## Local Development

Simply open `index.html` in your browser:

```bash
# Using Python's built-in server
python -m http.server 8000 --directory website

# Using Node's http-server
npx http-server website -p 8000

# Or just open the file directly
open website/index.html
```

Visit `http://localhost:8000` in your browser.

## Deployment

The website is automatically deployed to GitHub Pages when changes are pushed to the `main` branch.

### Manual Deployment

1. **Enable GitHub Pages** in repository settings:
   - Go to Settings → Pages
   - Source: GitHub Actions

2. **Push changes** to trigger deployment:
   ```bash
   git add website/
   git commit -m "docs: update website"
   git push origin main
   ```

3. **View your site**:
   - URL: `https://specpulse.xyz`
   - Automatic deployment from main branch

## Customization

### Colors

Edit the Tailwind config in `index.html`:

```javascript
tailwind.config = {
  theme: {
    extend: {
      colors: {
        primary: { ... },
        secondary: { ... }
      }
    }
  }
}
```

### Content

All content is in `index.html`:
- Hero section
- Features
- Getting Started guide
- Documentation links
- Footer

### Interactivity

Alpine.js components are inline in the HTML:

```html
<div x-data="{ count: 0 }">
  <button @click="count++">Click me</button>
  <span x-text="count"></span>
</div>
```

## Tech Stack

- **Tailwind CSS 3.x** - via CDN
- **Alpine.js 3.x** - via CDN
- **Google Fonts** - Inter & JetBrains Mono
- **Pure HTML** - no build process

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## License

MIT License - see [LICENSE](../LICENSE) for details
