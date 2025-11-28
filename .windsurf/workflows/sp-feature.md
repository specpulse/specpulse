---
description: Initialize a new feature with SpecPulse framework (alias for sp-pulse) using SDD methodology
auto_execution_mode: 3
---

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the feature initialization outcome
- Only edit files in specs/, plans/, tasks/, memory/ directories - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use `specpulse feature init <feature-name>` when available
- **FALLBACK**: File Operations only if CLI fails
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/
- **EDITABLE ONLY**: specs/, plans/, tasks/, memory/

**Note: This command is an alias for `/sp-pulse` but provides a more intuitive name for feature initialization**

**Steps**
Track these steps as TODOs and complete them one by one.

1. **Validate arguments** and extract feature name + optional ID
2. **Try CLI first**:
   ```bash
   specpulse feature init <feature-name>
   ```
   If this succeeds, STOP HERE. CLI handles everything.

3. **If CLI doesn't exist, use File Operations**:
   - **Step 1: Determine Feature ID**
     - Read specs/ directory (list subdirectories)
     - Find highest number (e.g., 001, 002) and increment
     - Or use 001 if no features exist
   - **Step 2: Create Feature Directories Using Bash**
     ```bash
     mkdir -p specs/001-feature-name
     mkdir -p plans/001-feature-name
     mkdir -p tasks/001-feature-name
     ```
   - **Step 3: Update Context File**
     - Read: memory/context.md
     - Edit: memory/context.md (Add new feature entry with ID, name, timestamp)
   - **Step 4: Create Git Branch (Optional)**
     ```bash
     git checkout -b 001-feature-name
     ```

4. **Intelligent specification suggestions**:
   - Analyze feature name to infer project type and complexity
   - Generate 3 context-aware specification suggestions:
     1. **Core specification** (essential functionality only)
     2. **Standard specification** (comprehensive with detailed requirements)
     3. **Complete specification** (full-featured with all aspects)
   - Show estimated development time for each option
   - Guide user to `/sp-spec [chosen-option]` after selection

5. **Validate structure** and report comprehensive status

**Usage**
```
/sp-feature <feature-name> [feature-id]
```

**Examples**

**Web application feature:**
```
/sp-feature user-dashboard
```
Output:
```
## Feature Initialization: user-dashboard

### Project Analysis
- **Type**: Web Application Feature
- **Complexity**: Moderate
- **Estimated Timeline**: 8-12 hours (Standard spec)

### Directory Structure Created
✓ specs/001-user-dashboard/
✓ plans/001-user-dashboard/
✓ tasks/001-user-dashboard/

### Context Updated
- **Current Feature**: 001-user-dashboard
- **Git Branch**: 001-user-dashboard (created)
- **Status**: Ready for specification

### Specification Suggestions

**1. Core Specification** (2-4 hours)
Essential dashboard functionality:
- User profile display
- Basic navigation
- Session management

**2. Standard Specification** (8-12 hours) ← **Recommended**
Comprehensive dashboard features:
- User profile with editing
- Activity history
- Settings management
- Responsive design
- Basic analytics

**3. Complete Specification** (16-24 hours)
Full-featured dashboard:
- Advanced user profiles
- Real-time notifications
- Custom widgets
- Theme customization
- Advanced analytics
- Multi-language support

### Next Steps
Choose specification approach:
`/sp-spec core` | `/sp-spec standard` | `/sp-spec complete`

Or provide custom description:
`/sp-spec "user dashboard with profile editing and activity tracking"`
```

**API service feature:**
```
/sp-feature payment-api
```
Output:
```
## Feature Initialization: payment-api

### Project Analysis
- **Type**: REST API Service
- **Complexity**: High
- **Estimated Timeline**: 16-24 hours (Complete spec)

### Directory Structure Created
✓ specs/002-payment-api/
✓ plans/002-payment-api/
✓ tasks/002-payment-api/

### Specification Suggestions

**1. Core Specification** (4-6 hours)
Basic payment processing:
- Payment creation
- Status tracking
- Simple validation

**2. Standard Specification** (12-16 hours)
Robust payment API:
- Multiple payment methods
- Refund processing
- Webhook support
- Error handling

**3. Complete Specification** (20-30 hours) ← **Recommended**
Enterprise payment system:
- Multiple payment gateways
- Advanced security
- Subscription billing
- Fraud detection
- Comprehensive reporting
- Rate limiting

### Next Steps
`/sp-spec complete` for enterprise-grade payment API
```

**Mobile app component:**
```
/sp-feature notification-system
```
Output:
```
## Feature Initialization: notification-system

### Project Analysis
- **Type**: Mobile/Web Component
- **Complexity**: Moderate
- **Estimated Timeline**: 8-12 hours

### Specification Suggestions

**1. Core Specification** (3-5 hours)
Basic notifications:
- Push notifications
- In-app alerts
- Simple management

**2. Standard Specification** (8-12 hours) ← **Recommended**
Full notification system:
- Push/in-app/email notifications
- User preferences
- Scheduling
- Templates

**3. Complete Specification** (15-20 hours)
Advanced notification platform:
- Multi-channel delivery
- A/B testing
- Analytics
- Automation rules
```

**With custom feature ID:**
```
/sp-feature authentication 005
```
Output:
```
## Feature Initialization: authentication

### Custom Feature ID
Using specified ID: 005-authentication

### Directory Structure Created
✓ specs/005-authentication/
✓ plans/005-authentication/
✓ tasks/005-authentication/
```

**Specification Intelligence**

**Project Type Detection:**
- **Web App**: Frontend-focused features (dashboard, UI components)
- **API Service**: Backend services (payment, user management, data processing)
- **Mobile App**: Mobile-specific features (notifications, offline sync)
- **Database System**: Data-focused features (migration, analytics)
- **Integration**: Third-party integrations (OAuth, payment gateways)

**Complexity Assessment:**
- **Simple**: Single responsibility, few dependencies
- **Moderate**: Multiple components, some external integrations
- **Complex**: Multiple services, advanced security, enterprise requirements

**Time Estimates:**
- **Core**: Essential functionality only
- **Standard**: Comprehensive features with good UX
- **Complete**: Enterprise-grade with advanced features

**Integration Workflow**

After feature initialization, continue with:

```bash
# Create specification
/sp-spec standard              # Use standard specification approach

# Generate implementation plan
/sp-plan                       # Create detailed implementation plan

# Break down into tasks
/sp-task                       # Generate task breakdown

# Execute tasks
/sp-execute                    # Start development
```

**CLI Integration**

**Try CLI First:**
```bash
specpulse feature init <feature-name>
specpulse sp-pulse init <feature-name>
```

**Fallback to Manual Feature Creation if CLI Fails:**
1. Determine feature ID
2. Create directory structure
3. Update context file
4. Create git branch
5. Generate specification suggestions

**Advanced Features**

**Smart Context Detection:**
- Analyzes existing project structure
- Detects technology stack
- Suggests consistent naming conventions
- Maintains project standards

**Template Integration:**
- Uses project-specific templates if available
- Falls back to standard SpecPulse templates
- Supports custom template directories

**Multi-Project Support:**
- Handles multiple feature development
- Maintains separate contexts
- Supports feature dependencies
- Tracks cross-feature integration

**Error Handling**

**Validation Errors:**
- Feature name sanitization (alphanumeric, hyphens only)
- Directory creation validation
- Git repository validation
- Template existence verification

**Recovery Options:**
- Automatic cleanup on failure
- Partial feature recovery
- Context file repair
- Git branch management

**Feature Categories**

**Common Feature Types:**
- **User Management**: Authentication, profiles, permissions
- **Data Management**: CRUD operations, migrations, analytics
- **Integration**: Third-party services, APIs, webhooks
- **UI Components**: Dashboards, forms, navigation
- **Business Logic**: Workflows, rules, processing
- **Infrastructure**: Deployment, monitoring, security

**Reference**
- Use `specpulse feature init --help` if you need additional CLI options
- Check `memory/context.md` for current feature context
- Run `specpulse doctor` if you encounter system issues
- This command is an alias for `/sp-pulse` with identical functionality
- After feature creation, continue with `/sp-spec` for specification development
<!-- SPECPULSE:END -->