// Netlify CMS Integration Script
// This script handles dynamic content loading from CMS data

class CMSIntegration {
    constructor() {
        this.dataPath = '_data/';
        this.init();
    }

    async init() {
        // Load site configuration
        await this.loadSiteConfig();
        
        // Load page-specific content
        const currentPage = this.getCurrentPage();
        switch(currentPage) {
            case 'index':
                await this.loadHomepage();
                break;
            case 'team':
                await this.loadTeamPage();
                break;
            case 'services':
                await this.loadServicesPage();
                break;
            case 'blogs':
                await this.loadBlogsPage();
                break;
        }
    }

    getCurrentPage() {
        const path = window.location.pathname;
        if (path === '/' || path.includes('index.html')) return 'index';
        if (path.includes('team.html')) return 'team';
        if (path.includes('services.html')) return 'services';
        if (path.includes('blogs.html')) return 'blogs';
        return 'other';
    }

    async loadSiteConfig() {
        try {
            const response = await fetch(`${this.dataPath}site.yml`);
            if (response.ok) {
                const config = await this.parseYAML(await response.text());
                this.updateSiteConfig(config);
            }
        } catch (error) {
            console.log('Using default site configuration');
        }
    }

    async loadHomepage() {
        try {
            const [homepageData, teamData, servicesData] = await Promise.all([
                this.loadYAMLFile('homepage.yml'),
                this.loadTeamData(),
                this.loadServicesData()
            ]);

            if (homepageData) this.updateHomepage(homepageData);
            if (teamData) this.updateHomepageTeam(teamData);
            if (servicesData) this.updateHomepageServices(servicesData);
        } catch (error) {
            console.log('Using default homepage content');
        }
    }

    async loadTeamPage() {
        try {
            const teamData = await this.loadTeamData();
            if (teamData) this.updateTeamPage(teamData);
        } catch (error) {
            console.log('Using default team content');
        }
    }

    async loadServicesPage() {
        try {
            const servicesData = await this.loadServicesData();
            if (servicesData) this.updateServicesPage(servicesData);
        } catch (error) {
            console.log('Using default services content');
        }
    }

    async loadBlogsPage() {
        try {
            const blogsData = await this.loadBlogsData();
            if (blogsData) this.updateBlogsPage(blogsData);
        } catch (error) {
            console.log('Using default blogs content');
        }
    }

    async loadYAMLFile(filename) {
        try {
            const response = await fetch(`${this.dataPath}${filename}`);
            if (response.ok) {
                return await this.parseYAML(await response.text());
            }
        } catch (error) {
            return null;
        }
    }

    async loadTeamData() {
        // Load all team member files
        const teamMembers = [];
        try {
            // This would need to be implemented with a directory listing
            // For now, we'll use the known team members
            const knownMembers = [
                'abhishek-divakar.yml',
                'akshita-satish.yml',
                'shalu-jain.yml',
                'dolly-kumar.yml'
            ];

            for (const memberFile of knownMembers) {
                const member = await this.loadYAMLFile(`team/${memberFile}`);
                if (member) teamMembers.push(member);
            }

            return teamMembers.sort((a, b) => (a.order || 999) - (b.order || 999));
        } catch (error) {
            return null;
        }
    }

    async loadServicesData() {
        // Load all service files
        const services = [];
        try {
            const knownServices = [
                'information-security.yml',
                'grc-advisory.yml',
                'digital-forensics.yml'
            ];

            for (const serviceFile of knownServices) {
                const service = await this.loadYAMLFile(`services/${serviceFile}`);
                if (service) services.push(service);
            }

            return services.sort((a, b) => (a.order || 999) - (b.order || 999));
        } catch (error) {
            return null;
        }
    }

    async loadBlogsData() {
        // Load all blog files
        const blogs = [];
        try {
            // This would need to be implemented with a directory listing
            // For now, return null to use default content
            return null;
        } catch (error) {
            return null;
        }
    }

    parseYAML(yamlText) {
        // Simple YAML parser for basic key-value pairs
        // In production, you'd use a proper YAML parser
        const lines = yamlText.split('\n');
        const result = {};
        let currentKey = null;
        let currentArray = null;

        for (const line of lines) {
            const trimmed = line.trim();
            if (!trimmed || trimmed.startsWith('#')) continue;

            if (trimmed.includes(':') && !trimmed.startsWith('-')) {
                const [key, ...valueParts] = trimmed.split(':');
                const value = valueParts.join(':').trim();
                
                if (value.startsWith('"') && value.endsWith('"')) {
                    result[key.trim()] = value.slice(1, -1);
                } else if (value) {
                    result[key.trim()] = value;
                } else {
                    currentKey = key.trim();
                    currentArray = [];
                    result[currentKey] = currentArray;
                }
            } else if (trimmed.startsWith('-') && currentArray) {
                currentArray.push(trimmed.substring(1).trim());
            }
        }

        return result;
    }

    updateSiteConfig(config) {
        // Update site-wide elements
        if (config.title) {
            document.title = config.title;
            const brandElements = document.querySelectorAll('.navbar-brand');
            brandElements.forEach(el => {
                const textNode = el.childNodes[el.childNodes.length - 1];
                if (textNode && textNode.nodeType === Node.TEXT_NODE) {
                    textNode.textContent = config.title;
                }
            });
        }

        if (config.email) {
            const emailLinks = document.querySelectorAll('a[href^="mailto:"]');
            emailLinks.forEach(link => {
                link.href = `mailto:${config.email}`;
                if (link.textContent.includes('@')) {
                    link.textContent = config.email;
                }
            });
        }

        if (config.linkedin) {
            const linkedinLinks = document.querySelectorAll('a[href*="linkedin.com/company"]');
            linkedinLinks.forEach(link => link.href = config.linkedin);
        }
    }

    updateHomepage(data) {
        // Update hero section
        if (data.hero_title) {
            const heroTitle = document.querySelector('.hero-title');
            if (heroTitle) heroTitle.textContent = data.hero_title;
        }

        if (data.hero_subtitle) {
            const heroSubtitle = document.querySelector('.hero-subtitle');
            if (heroSubtitle) heroSubtitle.textContent = data.hero_subtitle;
        }

        // Update sections
        if (data.core_services) {
            const servicesTitle = document.querySelector('.services-overview h2');
            const servicesSubtitle = document.querySelector('.services-overview .lead');
            if (servicesTitle) servicesTitle.textContent = data.core_services.title;
            if (servicesSubtitle) servicesSubtitle.textContent = data.core_services.subtitle;
        }

        if (data.team_section) {
            const teamTitle = document.querySelector('.team-section h2');
            const teamSubtitle = document.querySelector('.team-section .lead');
            if (teamTitle) teamTitle.textContent = data.team_section.title;
            if (teamSubtitle) teamSubtitle.textContent = data.team_section.subtitle;
        }

        if (data.cta_section) {
            const ctaTitle = document.querySelector('.cta-section h2');
            const ctaSubtitle = document.querySelector('.cta-section .lead');
            const ctaButton = document.querySelector('.cta-section .btn');
            if (ctaTitle) ctaTitle.textContent = data.cta_section.title;
            if (ctaSubtitle) ctaSubtitle.textContent = data.cta_section.subtitle;
            if (ctaButton) ctaButton.textContent = data.cta_section.button_text;
        }
    }

    updateHomepageTeam(teamData) {
        const teamContainer = document.querySelector('.team-section .row:last-child');
        if (!teamContainer || !teamData) return;

        // Clear existing team members
        teamContainer.innerHTML = '';

        // Add featured team members
        const featuredMembers = teamData.filter(member => member.featured);
        featuredMembers.forEach(member => {
            const memberHTML = `
                <div class="col-md-3 mb-4">
                    <div class="team-card text-center">
                        <img src="${member.photo}" alt="${member.name}" class="team-photo">
                        <h4>${member.name}</h4>
                        <p class="team-role">${member.role}</p>
                        <a href="${member.linkedin}" target="_blank" class="btn btn-sm btn-linkedin">
                            LinkedIn Profile
                        </a>
                    </div>
                </div>
            `;
            teamContainer.insertAdjacentHTML('beforeend', memberHTML);
        });
    }

    updateHomepageServices(servicesData) {
        const servicesContainer = document.querySelector('.services-overview .row:last-child');
        if (!servicesContainer || !servicesData) return;

        // Clear existing services
        servicesContainer.innerHTML = '';

        // Add featured services
        const featuredServices = servicesData.filter(service => service.featured).slice(0, 3);
        featuredServices.forEach(service => {
            const serviceHTML = `
                <div class="col-md-4 mb-4">
                    <div class="service-card">
                        <div class="service-icon">${service.icon}</div>
                        <h4>${service.title}</h4>
                        <p>${service.short_description}</p>
                        <a href="${service.url}" class="btn btn-outline-primary">Learn More</a>
                    </div>
                </div>
            `;
            servicesContainer.insertAdjacentHTML('beforeend', serviceHTML);
        });
    }

    updateTeamPage(teamData) {
        const teamContainer = document.querySelector('.team-section .row');
        if (!teamContainer || !teamData) return;

        // Clear existing team members
        teamContainer.innerHTML = '';

        // Add all team members
        teamData.forEach(member => {
            const skillsHTML = member.skills ? member.skills.map(skill => 
                `<span class="skill-tag">${skill}</span>`
            ).join('') : '';

            const memberHTML = `
                <div class="col-md-4 mb-5">
                    <div class="team-card text-center">
                        <img src="${member.photo}" alt="${member.name}" class="team-photo">
                        <h4>${member.name}</h4>
                        <p class="team-role">${member.role}</p>
                        <p class="team-bio">${member.bio}</p>
                        <div class="team-skills">
                            ${skillsHTML}
                        </div>
                        <a href="${member.linkedin}" target="_blank" class="btn btn-linkedin mt-3">
                            <i class="fab fa-linkedin"></i> Connect on LinkedIn
                        </a>
                    </div>
                </div>
            `;
            teamContainer.insertAdjacentHTML('beforeend', memberHTML);
        });
    }

    updateServicesPage(servicesData) {
        const servicesContainer = document.querySelector('.services-grid .row, .py-5 .row');
        if (!servicesContainer || !servicesData) return;

        // Clear existing services
        servicesContainer.innerHTML = '';

        // Add all services
        servicesData.forEach(service => {
            const serviceHTML = `
                <div class="col-md-4 mb-4">
                    <div class="service-card h-100">
                        <div class="service-icon">${service.icon}</div>
                        <h4>${service.title}</h4>
                        <p>${service.short_description}</p>
                        <a href="${service.url}" class="btn btn-outline-primary">Learn More</a>
                    </div>
                </div>
            `;
            servicesContainer.insertAdjacentHTML('beforeend', serviceHTML);
        });
    }

    updateBlogsPage(blogsData) {
        // Implementation for blogs page updates
        // This would be similar to other update methods
    }
}

// Initialize CMS integration when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new CMSIntegration();
});