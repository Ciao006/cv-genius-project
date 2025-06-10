import React, { useState } from 'react';
import { Check, Eye, Sparkles, Crown, Zap } from 'lucide-react';
import Button from '@/components/ui/Button';

interface Template {
  id: string;
  name: string;
  description: string;
  category: 'classic' | 'modern' | 'creative' | 'executive';
  isPremium: boolean;
  preview: string;
  features: string[];
  colors: string[];
  atsScore: number;
}

interface TemplateSelectorProps {
  selectedTemplate: string;
  onTemplateSelect: (templateId: string) => void;
  onClose?: () => void;
}

const TemplateSelector: React.FC<TemplateSelectorProps> = ({
  selectedTemplate,
  onTemplateSelect,
  onClose
}) => {
  const [activeCategory, setActiveCategory] = useState<string>('all');
  const [hoveredTemplate, setHoveredTemplate] = useState<string | null>(null);

  const templates: Template[] = [
    {
      id: 'professional',
      name: 'Professional',
      description: 'Clean, traditional layout perfect for corporate roles',
      category: 'classic',
      isPremium: false,
      preview: 'professional-preview',
      features: ['ATS-Optimized', 'Traditional Layout', 'Corporate-Friendly'],
      colors: ['#2563eb', '#1f2937', '#374151'],
      atsScore: 95
    },
    {
      id: 'modern',
      name: 'Modern Executive',
      description: 'Contemporary design with elegant typography',
      category: 'modern',
      isPremium: false,
      preview: 'modern-preview',
      features: ['Clean Design', 'Modern Typography', 'Balanced Layout'],
      colors: ['#059669', '#064e3b', '#1f2937'],
      atsScore: 90
    },
    {
      id: 'creative',
      name: 'Creative Pro',
      description: 'Stand out with this visually appealing design',
      category: 'creative',
      isPremium: true,
      preview: 'creative-preview',
      features: ['Visual Elements', 'Color Accents', 'Creative Layout'],
      colors: ['#7c3aed', '#a855f7', '#ec4899'],
      atsScore: 75
    },
    {
      id: 'tech',
      name: 'Tech Specialist',
      description: 'Perfect for technology and engineering roles',
      category: 'modern',
      isPremium: true,
      preview: 'tech-preview',
      features: ['Tech-Focused', 'Skill Highlights', 'Project Showcase'],
      colors: ['#0ea5e9', '#06b6d4', '#10b981'],
      atsScore: 88
    },
    {
      id: 'executive',
      name: 'Executive Leadership',
      description: 'Sophisticated design for senior-level positions',
      category: 'executive',
      isPremium: true,
      preview: 'executive-preview',
      features: ['Premium Design', 'Leadership Focus', 'Achievement Highlight'],
      colors: ['#1f2937', '#374151', '#6b7280'],
      atsScore: 92
    },
    {
      id: 'minimalist',
      name: 'Minimalist',
      description: 'Simple, clean design that focuses on content',
      category: 'classic',
      isPremium: false,
      preview: 'minimalist-preview',
      features: ['Minimal Design', 'Content-Focused', 'High Readability'],
      colors: ['#000000', '#374151', '#6b7280'],
      atsScore: 98
    }
  ];

  const categories = [
    { id: 'all', label: 'All Templates', count: templates.length },
    { id: 'classic', label: 'Classic', count: templates.filter(t => t.category === 'classic').length },
    { id: 'modern', label: 'Modern', count: templates.filter(t => t.category === 'modern').length },
    { id: 'creative', label: 'Creative', count: templates.filter(t => t.category === 'creative').length },
    { id: 'executive', label: 'Executive', count: templates.filter(t => t.category === 'executive').length }
  ];

  const filteredTemplates = activeCategory === 'all' 
    ? templates 
    : templates.filter(t => t.category === activeCategory);

  const generateTemplateHTML = (template: Template) => {
    const primaryColor = template.colors[0];
    const secondaryColor = template.colors[1];
    
    return `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Inter', 'Segoe UI', sans-serif;
      line-height: 1.5;
      color: #2d3748;
      background: white;
      padding: 30px;
      font-size: 12px;
    }
    .header {
      ${template.id === 'creative' ? `
        background: linear-gradient(135deg, ${primaryColor}15 0%, ${primaryColor}05 100%);
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 25px;
      ` : `
        text-align: ${template.id === 'minimalist' ? 'left' : 'center'};
        border-bottom: ${template.id === 'professional' ? '3px solid ' + primaryColor : '2px solid #e2e8f0'};
        padding-bottom: 20px;
        margin-bottom: 25px;
      `}
    }
    .name {
      font-size: ${template.id === 'executive' ? '28px' : '24px'};
      font-weight: ${template.id === 'minimalist' ? '400' : '700'};
      color: ${template.id === 'minimalist' ? '#1a202c' : primaryColor};
      margin-bottom: 8px;
      ${template.id === 'creative' ? 'background: linear-gradient(45deg, ' + primaryColor + ', ' + template.colors[2] + '); -webkit-background-clip: text; -webkit-text-fill-color: transparent;' : ''}
    }
    .contact {
      font-size: 13px;
      color: #4a5568;
      ${template.id === 'tech' ? 'font-family: monospace;' : ''}
    }
    .section {
      margin-bottom: 25px;
    }
    .section-title {
      font-size: 16px;
      font-weight: 600;
      color: ${primaryColor};
      margin-bottom: 12px;
      ${template.id === 'creative' ? `
        background: ${primaryColor};
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        display: inline-block;
      ` : template.id === 'executive' ? `
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 14px;
        border-bottom: 2px solid ${primaryColor};
        padding-bottom: 5px;
      ` : `
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 5px;
      `}
    }
    .content {
      font-size: 12px;
      line-height: 1.6;
      color: #4a5568;
    }
    .item {
      margin-bottom: 15px;
      ${template.id === 'tech' ? `
        background: #f8fafc;
        padding: 12px;
        border-radius: 6px;
        border-left: 3px solid ${primaryColor};
      ` : ''}
    }
    .item-title {
      font-weight: 600;
      color: #2d3748;
      margin-bottom: 3px;
    }
    .item-meta {
      font-size: 11px;
      color: #718096;
      margin-bottom: 5px;
    }
    ${template.id === 'modern' ? `
      .section:nth-child(even) { background: #f8fafc; padding: 15px; border-radius: 8px; }
    ` : ''}
  </style>
</head>
<body>
  <div class="header">
    <div class="name">John Doe</div>
    <div class="contact">john.doe@email.com • +1 (555) 123-4567 • New York, NY</div>
  </div>
  
  <div class="section">
    <div class="section-title">Professional Summary</div>
    <div class="content">
      Experienced software engineer with 5+ years developing scalable web applications. 
      Proven track record of delivering high-quality solutions and leading cross-functional teams.
    </div>
  </div>
  
  <div class="section">
    <div class="section-title">Experience</div>
    <div class="item">
      <div class="item-title">Senior Software Engineer</div>
      <div class="item-meta">Tech Company Inc. | 2020 - Present</div>
      <div class="content">Led development of core platform features serving 100k+ users</div>
    </div>
    <div class="item">
      <div class="item-title">Software Engineer</div>
      <div class="item-meta">StartupCo | 2018 - 2020</div>
      <div class="content">Built and maintained microservices architecture</div>
    </div>
  </div>
  
  <div class="section">
    <div class="section-title">Skills</div>
    <div class="content">
      JavaScript • React • Node.js • Python • AWS • Docker • PostgreSQL
    </div>
  </div>
</body>
</html>`;
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-6xl w-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="p-6 border-b border-gray-200 bg-gradient-to-r from-blue-50 to-purple-50">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Choose Your Template</h2>
              <p className="text-gray-600">Select a professional template that matches your style and industry</p>
            </div>
            <Button variant="ghost" onClick={onClose} className="text-gray-500 hover:text-gray-700">
              ×
            </Button>
          </div>
        </div>

        <div className="flex h-[calc(90vh-120px)]">
          {/* Sidebar Categories */}
          <div className="w-64 bg-gray-50 border-r border-gray-200 p-4">
            <div className="space-y-2">
              {categories.map((category) => (
                <button
                  key={category.id}
                  onClick={() => setActiveCategory(category.id)}
                  className={`w-full flex items-center justify-between p-3 rounded-lg text-left transition-colors ${
                    activeCategory === category.id
                      ? 'bg-blue-100 text-blue-700 border border-blue-200'
                      : 'hover:bg-gray-100 text-gray-700'
                  }`}
                >
                  <span className="font-medium">{category.label}</span>
                  <span className="text-sm bg-gray-200 text-gray-600 px-2 py-1 rounded-full">
                    {category.count}
                  </span>
                </button>
              ))}
            </div>

            <div className="mt-6 p-4 bg-gradient-to-r from-blue-100 to-purple-100 rounded-lg">
              <div className="flex items-center gap-2 mb-2">
                <Crown className="w-4 h-4 text-yellow-600" />
                <span className="font-semibold text-gray-900">Premium</span>
              </div>
              <p className="text-xs text-gray-600 mb-3">
                Unlock all templates and advanced features
              </p>
              <Button size="sm" className="w-full bg-gradient-to-r from-yellow-400 to-orange-500">
                Upgrade Now
              </Button>
            </div>
          </div>

          {/* Templates Grid */}
          <div className="flex-1 overflow-y-auto p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredTemplates.map((template) => (
                <div
                  key={template.id}
                  className={`relative group cursor-pointer transition-all duration-300 ${
                    selectedTemplate === template.id
                      ? 'ring-2 ring-blue-500 shadow-lg scale-105'
                      : 'hover:shadow-lg hover:scale-102'
                  }`}
                  onClick={() => onTemplateSelect(template.id)}
                  onMouseEnter={() => setHoveredTemplate(template.id)}
                  onMouseLeave={() => setHoveredTemplate(null)}
                >
                  {/* Template Preview */}
                  <div className="bg-white border border-gray-200 rounded-lg overflow-hidden shadow-sm">
                    <div className="h-48 bg-gray-50 relative overflow-hidden">
                      <iframe
                        src={`data:text/html;charset=utf-8,${encodeURIComponent(generateTemplateHTML(template))}`}
                        className="w-full h-full scale-75 origin-top-left border-0"
                        style={{ width: '133%', height: '133%' }}
                        title={`${template.name} Preview`}
                      />
                      
                      {/* Overlay */}
                      <div className={`absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors ${
                        hoveredTemplate === template.id ? 'flex items-center justify-center' : ''
                      }`}>
                        {hoveredTemplate === template.id && (
                          <Button
                            variant="outline"
                            size="sm"
                            icon={<Eye className="w-4 h-4" />}
                            className="bg-white/90 backdrop-blur-sm"
                          >
                            Preview
                          </Button>
                        )}
                      </div>

                      {/* Premium Badge */}
                      {template.isPremium && (
                        <div className="absolute top-2 right-2 bg-gradient-to-r from-yellow-400 to-orange-500 text-white px-2 py-1 rounded-full text-xs font-semibold flex items-center gap-1">
                          <Crown className="w-3 h-3" />
                          Premium
                        </div>
                      )}

                      {/* Selected Badge */}
                      {selectedTemplate === template.id && (
                        <div className="absolute top-2 left-2 bg-blue-500 text-white p-1 rounded-full">
                          <Check className="w-4 h-4" />
                        </div>
                      )}
                    </div>

                    {/* Template Info */}
                    <div className="p-4">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="font-semibold text-gray-900">{template.name}</h3>
                        <div className="flex items-center gap-1">
                          <Zap className="w-3 h-3 text-green-500" />
                          <span className="text-xs font-medium text-green-600">
                            {template.atsScore}% ATS
                          </span>
                        </div>
                      </div>
                      
                      <p className="text-sm text-gray-600 mb-3">{template.description}</p>
                      
                      {/* Features */}
                      <div className="flex flex-wrap gap-1 mb-3">
                        {template.features.map((feature, index) => (
                          <span
                            key={index}
                            className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded-full"
                          >
                            {feature}
                          </span>
                        ))}
                      </div>

                      {/* Color Palette */}
                      <div className="flex items-center gap-2">
                        <span className="text-xs text-gray-500">Colors:</span>
                        <div className="flex gap-1">
                          {template.colors.map((color, index) => (
                            <div
                              key={index}
                              className="w-4 h-4 rounded-full border border-gray-200"
                              style={{ backgroundColor: color }}
                            />
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-gray-200 bg-gray-50 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Sparkles className="w-5 h-5 text-blue-500" />
            <span className="text-sm text-gray-600">
              All templates are ATS-optimized and professionally designed
            </span>
          </div>
          <div className="flex gap-3">
            <Button variant="outline" onClick={onClose}>
              Cancel
            </Button>
            <Button 
              onClick={() => onClose?.()}
              className="bg-blue-500 hover:bg-blue-600"
            >
              Apply Template
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TemplateSelector;