# Domain Setup - specpulse.xyz

This document outlines the configuration for SpecPulse's custom domain setup.

## Overview

- **Primary Domain**: [specpulse.xyz](https://specpulse.xyz)
- **Email Contact**: [info@specpulse.xyz](mailto:info@specpulse.xyz)
- **Security Contact**: [security@specpulse.xyz](mailto:security@specpulse.xyz)

## Configuration Files

### 1. GitHub Actions Workflow
- **File**: `.github/workflows/deploy-website.yml`
- **Purpose**: Automatic deployment to GitHub Pages with custom domain
- **Trigger**: Push to main branch, changes to website directory

### 2. Domain Configuration
- **File**: `website/CNAME`
- **Content**: `specpulse.xyz`
- **Purpose**: GitHub Pages custom domain configuration

### 3. Package Information
- **File**: `setup.py`
- **Updates**:
  - URL: `https://specpulse.xyz`
  - Author Email: `info@specpulse.xyz`
  - Project URLs with proper domain references

### 4. Documentation Updates
- **Files**: `README.md`, `website/README.md`, `website/index.html`
- **Changes**: All GitHub Pages references updated to `specpulse.xyz`
- **Contact**: Added `info@specpulse.xyz` contact information

## Deployment Process

### Automatic Deployment
1. Push changes to `main` branch
2. GitHub Actions automatically builds and deploys website
3. Domain configuration includes CNAME file
4. Site available at `https://specpulse.xyz`

### Manual Steps Required
1. **DNS Configuration**: Set up DNS records for specpulse.xyz
2. **GitHub Pages Settings**: Enable GitHub Pages in repository settings
3. **Custom Domain**: Add specpulse.xyz as custom domain in GitHub Pages settings
4. **SSL Certificate**: GitHub automatically provides SSL certificate

## Email Configuration

### Email Addresses
- **General Contact**: info@specpulse.xyz
- **Security**: security@specpulse.xyz

### Email Forwarding Setup
Configure email forwarding from your domain registrar to forward:
- info@specpulse.xyz → your personal email
- security@specpulse.xyz → your security contact email

## Files Updated

```
.github/workflows/deploy-website.yml    # New deployment workflow
.github/workflows/pages-setup.yml      # GitHub Pages setup
website/CNAME                          # Custom domain file
setup.py                               # Package metadata
README.md                              # Documentation with new domain
website/README.md                      # Website deployment documentation
website/index.html                     # Footer and contact updates
SECURITY.md                            # New security policy with domain
```

## Verification Checklist

- [ ] GitHub Actions workflow is enabled
- [ ] GitHub Pages is enabled in repository settings
- [ ] Custom domain `specpulse.xyz` is configured
- [ ] DNS records are pointing to GitHub Pages
- [ ] SSL certificate is active
- [ ] Email forwarding is configured
- [ ] All documentation references are updated
- [ ] Website is accessible at https://specpulse.xyz
- [ ] Contact forms are working

## Maintenance

### Regular Tasks
1. Monitor domain renewal
2. Verify SSL certificate status
3. Check email forwarding configuration
4. Update contact information as needed
5. Test GitHub Actions deployment regularly

### Troubleshooting
- **Domain not resolving**: Check DNS configuration
- **Deployment failures**: Check GitHub Actions logs
- **SSL issues**: Verify GitHub Pages settings
- **Email issues**: Check domain registrar email forwarding

---

**Last Updated**: November 28, 2025
**Version**: v2.7.0
**Contact**: [info@specpulse.xyz](mailto:info@specpulse.xyz)