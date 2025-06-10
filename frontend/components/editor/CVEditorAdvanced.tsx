import React, { useState, useRef } from 'react';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import { jsPDF } from 'jspdf';
import html2canvas from 'html2canvas';

// CV Templates
const CV_TEMPLATES = {
  modern: {
    name: 'Modern',
    headerBg: '#3182ce',
    headerColor: 'white',
    accentColor: '#3182ce',
    fontSize: { header: '32px', title: '24px', body: '16px' },
    font: "'Inter', sans-serif"
  },
  classic: {
    name: 'Classic',
    headerBg: 'white',
    headerColor: '#1a202c',
    accentColor: '#2d3748',
    fontSize: { header: '28px', title: '20px', body: '15px' },
    font: "'Times New Roman', serif"
  },
  minimal: {
    name: 'Minimal',
    headerBg: 'white',
    headerColor: '#000',
    accentColor: '#000',
    fontSize: { header: '26px', title: '18px', body: '14px' },
    font: "'Helvetica', sans-serif"
  },
  creative: {
    name: 'Creative',
    headerBg: '#6b46c1',
    headerColor: 'white',
    accentColor: '#6b46c1',
    fontSize: { header: '36px', title: '22px', body: '16px' },
    font: "'Poppins', sans-serif"
  }
};

interface CVData {
  personal_details: {
    full_name: string;
    email: string;
    phone: string;
    linkedin_url?: string;
    location?: string;
    desired_position?: string;
  };
  professional_summary: string;
  skills: {
    technical?: string[];
    soft?: string[];
    languages?: string[];
  };
  work_experience: Array<{
    id?: string;
    job_title: string;
    company: string;
    start_date: string;
    end_date?: string;
    is_current?: boolean;
    location?: string;
    achievements: string[];
  }>;
  education: Array<{
    id?: string;
    degree: string;
    institution: string;
    start_date: string;
    end_date?: string;
    grade?: string;
    location?: string;
  }>;
}

interface Section {
  id: string;
  type: 'summary' | 'skills' | 'experience' | 'education';
  enabled: boolean;
}

interface CVEditorAdvancedProps {
  cvData: CVData;
  onUpdate?: (data: CVData) => void;
  isEditing?: boolean;
}

// Text improvement suggestions
const textSuggestions = {
  actionVerbs: ['Led', 'Managed', 'Developed', 'Implemented', 'Designed', 'Achieved', 'Improved', 'Created', 'Established', 'Increased'],
  metrics: ['Increased by X%', 'Reduced by X%', 'Managed team of X', 'Budget of $X', 'X+ years experience'],
  commonMistakes: {
    'responsible for': 'Led/Managed',
    'worked on': 'Developed/Created',
    'helped with': 'Contributed to',
    'in charge of': 'Directed/Oversaw'
  }
};

export default function CVEditorAdvanced({ cvData: initialData, onUpdate, isEditing = true }: CVEditorAdvancedProps) {
  const [cvData, setCvData] = useState<CVData>(() => {
    // Add IDs to experiences and education if not present
    return {
      ...initialData,
      work_experience: initialData.work_experience.map((exp, idx) => ({
        ...exp,
        id: exp.id || `exp-${idx}`
      })),
      education: initialData.education.map((edu, idx) => ({
        ...edu,
        id: edu.id || `edu-${idx}`
      }))
    };
  });
  
  const [history, setHistory] = useState<CVData[]>([cvData]);
  const [historyIndex, setHistoryIndex] = useState(0);
  const [selectedTemplate, setSelectedTemplate] = useState('modern');
  const [sections, setSections] = useState<Section[]>([
    { id: 'summary', type: 'summary', enabled: true },
    { id: 'skills', type: 'skills', enabled: true },
    { id: 'experience', type: 'experience', enabled: true },
    { id: 'education', type: 'education', enabled: true }
  ]);
  const [showDesignPanel, setShowDesignPanel] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [previewMode, setPreviewMode] = useState(false);
  const cvRef = useRef<HTMLDivElement>(null);

  // Handle section reordering
  const handleDragEnd = (result: any) => {
    if (!result.destination) return;

    const items = Array.from(sections);
    const [reorderedItem] = items.splice(result.source.index, 1);
    items.splice(result.destination.index, 0, reorderedItem);

    setSections(items);
  };

  // Toggle section visibility
  const toggleSection = (sectionId: string) => {
    setSections(sections.map(section => 
      section.id === sectionId 
        ? { ...section, enabled: !section.enabled }
        : section
    ));
  };

  // Update content handler
  const handleContentChange = (path: string[], value: any) => {
    const newData = { ...cvData };
    let current: any = newData;
    
    for (let i = 0; i < path.length - 1; i++) {
      current = current[path[i]];
    }
    
    current[path[path.length - 1]] = value;
    setCvData(newData);
    
    // Add to history
    const newHistory = history.slice(0, historyIndex + 1);
    newHistory.push(newData);
    setHistory(newHistory);
    setHistoryIndex(newHistory.length - 1);
    
    if (onUpdate) {
      onUpdate(newData);
    }
  };

  // Template switcher
  const handleTemplateChange = (templateKey: string) => {
    setSelectedTemplate(templateKey);
  };

  // Text improvement suggestion
  const getSuggestion = (text: string): string[] => {
    const suggestions: string[] = [];
    
    // Check for weak phrases
    Object.entries(textSuggestions.commonMistakes).forEach(([weak, strong]) => {
      if (text.toLowerCase().includes(weak)) {
        suggestions.push(`Replace "${weak}" with "${strong}"`);
      }
    });
    
    // Check for missing metrics
    if (!text.match(/\d+/)) {
      suggestions.push('Consider adding specific numbers or metrics');
    }
    
    // Suggest action verbs for achievements
    if (text.length < 50 && !textSuggestions.actionVerbs.some(verb => 
      text.startsWith(verb) || text.startsWith(verb.toLowerCase())
    )) {
      suggestions.push('Start with a strong action verb');
    }
    
    return suggestions;
  };

  const template = CV_TEMPLATES[selectedTemplate as keyof typeof CV_TEMPLATES];

  return (
    <div className="cv-editor-advanced">
      {/* Advanced Toolbar */}
      {isEditing && (
        <div className="editor-toolbar-advanced">
          <div className="toolbar-row">
            {/* History controls */}
            <div className="toolbar-section">
              <button onClick={() => {
                if (historyIndex > 0) {
                  setHistoryIndex(historyIndex - 1);
                  setCvData(history[historyIndex - 1]);
                }
              }} disabled={historyIndex === 0}>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6" />
                </svg>
                Undo
              </button>
              <button onClick={() => {
                if (historyIndex < history.length - 1) {
                  setHistoryIndex(historyIndex + 1);
                  setCvData(history[historyIndex + 1]);
                }
              }} disabled={historyIndex === history.length - 1}>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 10h-10a8 8 0 00-8 8v2M21 10l-6 6m6-6l-6-6" />
                </svg>
                Redo
              </button>
            </div>

            {/* Template selector */}
            <div className="toolbar-section">
              <button onClick={() => setShowDesignPanel(!showDesignPanel)} className="template-btn">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
                </svg>
                Templates & Design
              </button>
            </div>

            {/* Improvement suggestions */}
            <div className="toolbar-section">
              <button onClick={() => setShowSuggestions(!showSuggestions)} className="suggestions-btn">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                Improve Text
                {showSuggestions && <span className="suggestions-count">5</span>}
              </button>
            </div>

            {/* Preview toggle */}
            <div className="toolbar-section">
              <button onClick={() => setPreviewMode(!previewMode)} className={previewMode ? 'active' : ''}>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                {previewMode ? 'Edit Mode' : 'Preview'}
              </button>
            </div>

            {/* Export */}
            <div className="toolbar-section">
              <button onClick={async () => {
                if (!cvRef.current) return;
                const canvas = await html2canvas(cvRef.current, { scale: 2 });
                const pdf = new jsPDF('p', 'mm', 'a4');
                const imgWidth = 210;
                const imgHeight = (canvas.height * imgWidth) / canvas.width;
                pdf.addImage(canvas.toDataURL('image/png'), 'PNG', 0, 0, imgWidth, imgHeight);
                pdf.save(`${cvData.personal_details.full_name}_CV.pdf`);
              }} className="download-btn">
                Download PDF
              </button>
            </div>
          </div>

          {/* Design Panel */}
          {showDesignPanel && (
            <div className="design-panel">
              <h3>Choose Template</h3>
              <div className="template-grid">
                {Object.entries(CV_TEMPLATES).map(([key, tmpl]) => (
                  <div 
                    key={key} 
                    className={`template-card ${selectedTemplate === key ? 'active' : ''}`}
                    onClick={() => handleTemplateChange(key)}
                  >
                    <div className="template-preview" style={{ backgroundColor: tmpl.headerBg, color: tmpl.headerColor }}>
                      <div style={{ fontSize: '12px', fontFamily: tmpl.font }}>{tmpl.name}</div>
                    </div>
                    <span>{tmpl.name}</span>
                  </div>
                ))}
              </div>
              
              <h3 className="mt-4">Manage Sections</h3>
              <DragDropContext onDragEnd={handleDragEnd}>
                <Droppable droppableId="sections">
                  {(provided) => (
                    <div {...provided.droppableProps} ref={provided.innerRef} className="sections-list">
                      {sections.map((section, index) => (
                        <Draggable key={section.id} draggableId={section.id} index={index}>
                          {(provided, snapshot) => (
                            <div
                              ref={provided.innerRef}
                              {...provided.draggableProps}
                              {...provided.dragHandleProps}
                              className={`section-item ${snapshot.isDragging ? 'dragging' : ''}`}
                            >
                              <div className="section-controls">
                                <svg className="w-4 h-4 drag-handle" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8h16M4 16h16" />
                                </svg>
                                <span>{section.type.charAt(0).toUpperCase() + section.type.slice(1)}</span>
                                <label className="toggle-switch">
                                  <input 
                                    type="checkbox" 
                                    checked={section.enabled}
                                    onChange={() => toggleSection(section.id)}
                                  />
                                  <span className="slider"></span>
                                </label>
                              </div>
                            </div>
                          )}
                        </Draggable>
                      ))}
                      {provided.placeholder}
                    </div>
                  )}
                </Droppable>
              </DragDropContext>
            </div>
          )}

          {/* Text Improvement Panel */}
          {showSuggestions && (
            <div className="suggestions-panel">
              <h3>Text Improvement Suggestions</h3>
              <div className="suggestions-content">
                <div className="suggestion-category">
                  <h4>Action Verbs to Use:</h4>
                  <div className="suggestion-tags">
                    {textSuggestions.actionVerbs.map(verb => (
                      <span key={verb} className="suggestion-tag">{verb}</span>
                    ))}
                  </div>
                </div>
                <div className="suggestion-category">
                  <h4>Add Metrics:</h4>
                  <div className="suggestion-list">
                    {textSuggestions.metrics.map(metric => (
                      <div key={metric} className="suggestion-item">• {metric}</div>
                    ))}
                  </div>
                </div>
                <div className="suggestion-category">
                  <h4>Common Improvements:</h4>
                  <div className="suggestion-replacements">
                    {Object.entries(textSuggestions.commonMistakes).map(([weak, strong]) => (
                      <div key={weak} className="replacement-item">
                        <span className="weak">{weak}</span>
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                        </svg>
                        <span className="strong">{strong}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* CV Content with Template Styling */}
      <div ref={cvRef} className="resume-page-wrapper" style={{ fontFamily: template.font }}>
        {/* Header with template style */}
        <div className="header-holder" style={{ backgroundColor: template.headerBg, color: template.headerColor }}>
          <div className="resume-header">
            <h1 
              className="header-name"
              style={{ fontSize: template.fontSize.header, color: template.headerColor }}
              contentEditable={isEditing && !previewMode}
              suppressContentEditableWarning
              onBlur={(e) => handleContentChange(['personal_details', 'full_name'], e.currentTarget.textContent || '')}
            >
              {cvData.personal_details.full_name}
            </h1>
            {cvData.personal_details.desired_position && (
              <div 
                className="header-title"
                style={{ fontSize: template.fontSize.title, color: template.headerColor, opacity: 0.9 }}
                contentEditable={isEditing && !previewMode}
                suppressContentEditableWarning
                onBlur={(e) => handleContentChange(['personal_details', 'desired_position'], e.currentTarget.textContent || '')}
              >
                {cvData.personal_details.desired_position}
              </div>
            )}
            <div className="contact-info-container" style={{ fontSize: '14px' }}>
              <span 
                className="contact-info-item"
                contentEditable={isEditing && !previewMode}
                suppressContentEditableWarning
                onBlur={(e) => handleContentChange(['personal_details', 'phone'], e.currentTarget.textContent || '')}
              >
                {cvData.personal_details.phone}
              </span>
              <span 
                className="contact-info-item"
                contentEditable={isEditing && !previewMode}
                suppressContentEditableWarning
                onBlur={(e) => handleContentChange(['personal_details', 'email'], e.currentTarget.textContent || '')}
              >
                {cvData.personal_details.email}
              </span>
              {cvData.personal_details.linkedin_url && (
                <span 
                  className="contact-info-item"
                  contentEditable={isEditing && !previewMode}
                  suppressContentEditableWarning
                  onBlur={(e) => handleContentChange(['personal_details', 'linkedin_url'], e.currentTarget.textContent || '')}
                >
                  {cvData.personal_details.linkedin_url}
                </span>
              )}
              {cvData.personal_details.location && (
                <span 
                  className="contact-info-item"
                  contentEditable={isEditing && !previewMode}
                  suppressContentEditableWarning
                  onBlur={(e) => handleContentChange(['personal_details', 'location'], e.currentTarget.textContent || '')}
                >
                  {cvData.personal_details.location}
                </span>
              )}
            </div>
          </div>
        </div>

        <div className="resume-content">
          {/* Render sections in order */}
          {sections.filter(s => s.enabled).map(section => {
            switch (section.type) {
              case 'summary':
                return cvData.professional_summary ? (
                  <div key={section.id} className="section">
                    <h2 className="section-name" style={{ color: template.accentColor, borderColor: template.accentColor }}>
                      Summary
                    </h2>
                    <div 
                      className="summary-text"
                      style={{ fontSize: template.fontSize.body }}
                      contentEditable={isEditing && !previewMode}
                      suppressContentEditableWarning
                      onBlur={(e) => handleContentChange(['professional_summary'], e.currentTarget.textContent || '')}
                    >
                      {cvData.professional_summary}
                    </div>
                  </div>
                ) : null;

              case 'skills':
                return cvData.skills ? (
                  <div key={section.id} className="section">
                    <h2 className="section-name" style={{ color: template.accentColor, borderColor: template.accentColor }}>
                      Skills
                    </h2>
                    <div className="skills-container">
                      {Object.entries(cvData.skills).map(([category, skills]) => skills && skills.length > 0 && (
                        <div key={category} className="skill-row">
                          <div className="skill-category" style={{ fontSize: template.fontSize.body }}>
                            {category.charAt(0).toUpperCase() + category.slice(1)}:
                          </div>
                          <div className="skill-items">
                            {skills.map((skill, index) => (
                              <span 
                                key={index} 
                                className="skill-tag"
                                style={{ fontSize: template.fontSize.body }}
                                contentEditable={isEditing && !previewMode}
                                suppressContentEditableWarning
                                onBlur={(e) => {
                                  const newSkills = [...skills];
                                  newSkills[index] = e.currentTarget.textContent || '';
                                  handleContentChange(['skills', category], newSkills);
                                }}
                              >
                                {skill}
                              </span>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ) : null;

              case 'experience':
                return cvData.work_experience && cvData.work_experience.length > 0 ? (
                  <div key={section.id} className="section">
                    <h2 className="section-name" style={{ color: template.accentColor, borderColor: template.accentColor }}>
                      Experience
                    </h2>
                    {cvData.work_experience.map((exp, index) => (
                      <div key={exp.id} className="section-item">
                        <div className="item-header">
                          <div className="item-left">
                            <div 
                              className="item-position"
                              style={{ fontSize: template.fontSize.body }}
                              contentEditable={isEditing && !previewMode}
                              suppressContentEditableWarning
                              onBlur={(e) => {
                                const newExp = [...cvData.work_experience];
                                newExp[index].job_title = e.currentTarget.textContent || '';
                                handleContentChange(['work_experience'], newExp);
                              }}
                            >
                              {exp.job_title}
                            </div>
                            <div 
                              className="item-company"
                              style={{ fontSize: template.fontSize.body }}
                              contentEditable={isEditing && !previewMode}
                              suppressContentEditableWarning
                              onBlur={(e) => {
                                const newExp = [...cvData.work_experience];
                                newExp[index].company = e.currentTarget.textContent || '';
                                handleContentChange(['work_experience'], newExp);
                              }}
                            >
                              {exp.company}
                            </div>
                          </div>
                          <div>
                            <div className="item-dates" style={{ fontSize: template.fontSize.body }}>
                              {exp.start_date} - {exp.is_current ? 'Present' : exp.end_date}
                            </div>
                            {exp.location && <div className="item-location" style={{ fontSize: template.fontSize.body }}>{exp.location}</div>}
                          </div>
                        </div>
                        {exp.achievements && (
                          <ul className="achievements">
                            {exp.achievements.map((achievement, achIndex) => (
                              <li key={achIndex}>
                                <span className="bullet-dot" style={{ color: template.accentColor }}>•</span>
                                <span
                                  style={{ fontSize: template.fontSize.body }}
                                  contentEditable={isEditing && !previewMode}
                                  suppressContentEditableWarning
                                  onBlur={(e) => {
                                    const newExp = [...cvData.work_experience];
                                    newExp[index].achievements[achIndex] = e.currentTarget.textContent || '';
                                    handleContentChange(['work_experience'], newExp);
                                  }}
                                  onFocus={(e) => {
                                    if (showSuggestions) {
                                      const suggestions = getSuggestion(e.currentTarget.textContent || '');
                                      if (suggestions.length > 0) {
                                        // Show inline suggestions (you can implement a tooltip here)
                                        console.log('Suggestions:', suggestions);
                                      }
                                    }
                                  }}
                                >
                                  {achievement}
                                </span>
                              </li>
                            ))}
                          </ul>
                        )}
                      </div>
                    ))}
                  </div>
                ) : null;

              case 'education':
                return cvData.education && cvData.education.length > 0 ? (
                  <div key={section.id} className="section">
                    <h2 className="section-name" style={{ color: template.accentColor, borderColor: template.accentColor }}>
                      Education
                    </h2>
                    {cvData.education.map((edu, index) => (
                      <div key={edu.id} className="section-item">
                        <div className="item-header">
                          <div className="item-left">
                            <div 
                              className="item-position"
                              style={{ fontSize: template.fontSize.body }}
                              contentEditable={isEditing && !previewMode}
                              suppressContentEditableWarning
                              onBlur={(e) => {
                                const newEdu = [...cvData.education];
                                newEdu[index].degree = e.currentTarget.textContent || '';
                                handleContentChange(['education'], newEdu);
                              }}
                            >
                              {edu.degree}
                            </div>
                            <div 
                              className="item-company"
                              style={{ fontSize: template.fontSize.body }}
                              contentEditable={isEditing && !previewMode}
                              suppressContentEditableWarning
                              onBlur={(e) => {
                                const newEdu = [...cvData.education];
                                newEdu[index].institution = e.currentTarget.textContent || '';
                                handleContentChange(['education'], newEdu);
                              }}
                            >
                              {edu.institution}
                            </div>
                            {edu.grade && <div className="item-location" style={{ fontSize: template.fontSize.body }}>{edu.grade}</div>}
                          </div>
                          <div>
                            <div className="item-dates" style={{ fontSize: template.fontSize.body }}>
                              {edu.start_date}{edu.end_date && ` - ${edu.end_date}`}
                            </div>
                            {edu.location && <div className="item-location" style={{ fontSize: template.fontSize.body }}>{edu.location}</div>}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : null;

              default:
                return null;
            }
          })}
        </div>
      </div>

      <style jsx>{`
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');

        .cv-editor-advanced {
          max-width: 1400px;
          margin: 0 auto;
        }

        .editor-toolbar-advanced {
          background: #f7fafc;
          border: 1px solid #e2e8f0;
          border-radius: 12px;
          margin-bottom: 20px;
          overflow: hidden;
        }

        .toolbar-row {
          display: flex;
          justify-content: space-between;
          gap: 20px;
          padding: 16px 20px;
          flex-wrap: wrap;
        }

        .toolbar-section {
          display: flex;
          gap: 10px;
          align-items: center;
        }

        .editor-toolbar-advanced button {
          display: flex;
          align-items: center;
          gap: 6px;
          padding: 8px 16px;
          background: white;
          border: 1px solid #cbd5e0;
          border-radius: 6px;
          font-size: 14px;
          color: #2d3748;
          cursor: pointer;
          transition: all 0.2s;
          position: relative;
        }

        .editor-toolbar-advanced button:hover:not(:disabled) {
          background: #edf2f7;
          border-color: #a0aec0;
        }

        .editor-toolbar-advanced button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .editor-toolbar-advanced button.active {
          background: #3182ce;
          color: white;
          border-color: #3182ce;
        }

        .template-btn {
          background: #6b46c1 !important;
          color: white !important;
          border-color: #6b46c1 !important;
        }

        .suggestions-btn {
          background: #10b981 !important;
          color: white !important;
          border-color: #10b981 !important;
        }

        .suggestions-count {
          position: absolute;
          top: -8px;
          right: -8px;
          background: #ef4444;
          color: white;
          border-radius: 10px;
          padding: 2px 6px;
          font-size: 11px;
          font-weight: 600;
        }

        .download-btn {
          background: #3182ce !important;
          color: white !important;
          border-color: #3182ce !important;
        }

        /* Design Panel */
        .design-panel {
          padding: 20px;
          background: white;
          border-top: 1px solid #e2e8f0;
        }

        .design-panel h3 {
          font-size: 16px;
          font-weight: 600;
          margin-bottom: 12px;
          color: #2d3748;
        }

        .template-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
          gap: 12px;
          margin-bottom: 20px;
        }

        .template-card {
          cursor: pointer;
          text-align: center;
          transition: all 0.2s;
        }

        .template-card:hover {
          transform: translateY(-2px);
        }

        .template-card.active {
          transform: scale(1.05);
        }

        .template-preview {
          height: 80px;
          border-radius: 8px;
          display: flex;
          align-items: center;
          justify-content: center;
          margin-bottom: 8px;
          border: 2px solid transparent;
          transition: all 0.2s;
        }

        .template-card.active .template-preview {
          border-color: #3182ce;
          box-shadow: 0 0 0 3px rgba(49, 130, 206, 0.1);
        }

        .template-card span {
          font-size: 14px;
          color: #4a5568;
        }

        /* Sections Management */
        .sections-list {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .section-item {
          background: #f7fafc;
          border: 1px solid #e2e8f0;
          border-radius: 6px;
          padding: 12px;
          transition: all 0.2s;
        }

        .section-item.dragging {
          opacity: 0.5;
          background: #edf2f7;
        }

        .section-controls {
          display: flex;
          align-items: center;
          justify-content: space-between;
        }

        .drag-handle {
          cursor: grab;
          color: #a0aec0;
          margin-right: 12px;
        }

        /* Toggle Switch */
        .toggle-switch {
          position: relative;
          display: inline-block;
          width: 48px;
          height: 24px;
        }

        .toggle-switch input {
          opacity: 0;
          width: 0;
          height: 0;
        }

        .slider {
          position: absolute;
          cursor: pointer;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background-color: #cbd5e0;
          transition: .3s;
          border-radius: 24px;
        }

        .slider:before {
          position: absolute;
          content: "";
          height: 18px;
          width: 18px;
          left: 3px;
          bottom: 3px;
          background-color: white;
          transition: .3s;
          border-radius: 50%;
        }

        input:checked + .slider {
          background-color: #10b981;
        }

        input:checked + .slider:before {
          transform: translateX(24px);
        }

        /* Suggestions Panel */
        .suggestions-panel {
          padding: 20px;
          background: white;
          border-top: 1px solid #e2e8f0;
        }

        .suggestions-content {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 20px;
        }

        .suggestion-category {
          background: #f7fafc;
          padding: 16px;
          border-radius: 8px;
        }

        .suggestion-category h4 {
          font-size: 14px;
          font-weight: 600;
          margin-bottom: 12px;
          color: #2d3748;
        }

        .suggestion-tags {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
        }

        .suggestion-tag {
          background: #3182ce;
          color: white;
          padding: 4px 12px;
          border-radius: 4px;
          font-size: 13px;
          cursor: pointer;
          transition: all 0.2s;
        }

        .suggestion-tag:hover {
          background: #2c5282;
        }

        .suggestion-list {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .suggestion-item {
          font-size: 14px;
          color: #4a5568;
        }

        .suggestion-replacements {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .replacement-item {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 14px;
        }

        .replacement-item .weak {
          color: #ef4444;
          text-decoration: line-through;
        }

        .replacement-item .strong {
          color: #10b981;
          font-weight: 500;
        }

        .replacement-item svg {
          color: #a0aec0;
        }

        /* Resume Styles */
        .resume-page-wrapper {
          width: 210mm;
          min-height: 297mm;
          margin: 0 auto;
          background: white;
          box-shadow: 0 0 20px rgba(0,0,0,0.1);
          transition: all 0.3s;
        }

        @media screen and (max-width: 800px) {
          .resume-page-wrapper {
            width: 100%;
            box-shadow: none;
          }
        }

        .header-holder {
          padding: 20px 20px 10px;
          margin-bottom: 4px;
          transition: all 0.3s;
        }

        .resume-header {
          display: flex;
          flex-direction: column;
          align-items: center;
          text-align: center;
        }

        .header-name {
          font-weight: 700;
          margin-bottom: 4px;
          outline: none;
          transition: all 0.2s;
          padding: 2px 8px;
          border-radius: 4px;
        }

        .header-name:hover[contenteditable="true"] {
          background-color: rgba(255, 255, 255, 0.1);
        }

        .header-title {
          font-weight: 400;
          margin-bottom: 8px;
          outline: none;
          padding: 2px 8px;
          border-radius: 4px;
        }

        .header-title:hover[contenteditable="true"] {
          background-color: rgba(255, 255, 255, 0.1);
        }

        .contact-info-container {
          display: flex;
          flex-wrap: wrap;
          justify-content: center;
          align-items: center;
          gap: 10px;
        }

        .contact-info-item {
          position: relative;
          padding: 2px 10px;
          outline: none;
          transition: background-color 0.2s;
          border-radius: 4px;
        }

        .contact-info-item:hover[contenteditable="true"] {
          background-color: rgba(255, 255, 255, 0.1);
        }

        .contact-info-item:not(:last-child)::after {
          content: '|';
          position: absolute;
          right: -5px;
          opacity: 0.5;
        }

        .resume-content {
          padding: 0 20px 20px;
        }

        .section {
          margin-bottom: 20px;
          animation: fadeIn 0.3s ease-in;
        }

        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .section-name {
          font-weight: 600;
          border-bottom: 2px solid;
          padding-bottom: 4px;
          margin-bottom: 10px;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }

        .summary-text {
          line-height: 1.6;
          text-align: justify;
          outline: none;
          transition: background-color 0.2s;
          padding: 4px 8px;
          margin: -4px -8px;
          border-radius: 4px;
        }

        .summary-text:hover[contenteditable="true"] {
          background-color: #f0f4f8;
        }

        .section-item {
          margin-bottom: 16px;
          padding: 0;
        }

        .item-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 6px;
        }

        .item-left {
          flex: 1;
        }

        .item-position {
          font-weight: 600;
          margin-bottom: 2px;
          outline: none;
          transition: background-color 0.2s;
          padding: 2px 6px;
          margin: -2px -6px;
          border-radius: 4px;
        }

        .item-position:hover[contenteditable="true"] {
          background-color: #f0f4f8;
        }

        .item-company {
          opacity: 0.8;
          outline: none;
          transition: background-color 0.2s;
          padding: 2px 6px;
          margin: -2px -6px;
          border-radius: 4px;
        }

        .item-company:hover[contenteditable="true"] {
          background-color: #f0f4f8;
        }

        .item-dates {
          text-align: right;
          white-space: nowrap;
        }

        .item-location {
          text-align: right;
          opacity: 0.8;
        }

        .achievements {
          list-style: none;
          margin-top: 6px;
          padding-left: 0;
        }

        .achievements li {
          display: flex;
          align-items: flex-start;
          margin-bottom: 4px;
          line-height: 1.5;
        }

        .bullet-dot {
          margin-right: 8px;
          margin-top: 2px;
          flex-shrink: 0;
          font-weight: bold;
        }

        .achievements span:last-child {
          outline: none;
          flex: 1;
          transition: background-color 0.2s;
          padding: 2px 6px;
          margin: -2px -6px;
          border-radius: 4px;
          position: relative;
        }

        .achievements span:last-child:hover[contenteditable="true"] {
          background-color: #f0f4f8;
        }

        .skills-container {
          margin-top: 10px;
        }

        .skill-row {
          display: flex;
          align-items: center;
          margin-bottom: 8px;
        }

        .skill-category {
          font-weight: 500;
          min-width: 180px;
          margin-right: 20px;
        }

        .skill-items {
          display: flex;
          flex-wrap: wrap;
          gap: 6px;
        }

        .skill-tag {
          padding: 2px 8px;
          white-space: nowrap;
          outline: none;
          transition: background-color 0.2s;
          border-radius: 4px;
        }

        .skill-tag:hover[contenteditable="true"] {
          background-color: #f0f4f8;
        }

        .skill-tag:not(:last-child)::after {
          content: ',';
        }

        @media print {
          .editor-toolbar-advanced {
            display: none;
          }
          
          .resume-page-wrapper {
            width: 100%;
            margin: 0;
            box-shadow: none;
          }
          
          [contenteditable] {
            background: none !important;
          }
        }
      `}</style>
    </div>
  );
}