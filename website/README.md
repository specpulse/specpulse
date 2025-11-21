# SpecPulse Website

Modern, responsive landing page for SpecPulse built with:

- **Tailwind CSS** - Utility-first CSS framework
- **Alpine.js** - Lightweight JavaScript framework
- **shadcn-inspired** - Beautiful UI components

## Features

✨ **Modern Design**
- Clean, professional landing page
- Gradient accents and smooth animations
- Mobile-responsive layout

🎨 **UI Components**
- Hero section with call-to-action
- Feature cards with hover effects
- Code examples with syntax highlighting
- Statistics counters with animations
- Documentation links
- Responsive navigation

⚡ **Performance**
- Static HTML (no build step required)
- CDN-hosted dependencies
- Fast load times
- SEO-friendly

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
   - URL: `https://specpulse.github.io/specpulse/`
   - Or custom domain if configured

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
