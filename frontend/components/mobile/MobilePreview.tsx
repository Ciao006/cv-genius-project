import React, { useState } from 'react';
import { 
  XMarkIcon, 
  ArrowsPointingOutIcon, 
  DocumentArrowDownIcon,
  PencilIcon,
  ShareIcon 
} from '@heroicons/react/24/outline';

interface CVData {
  personal_details: {
    full_name: string;
    email: string;
    phone: string;
    location: string;
    linkedin_url: string;
    desired_position: string;
  };
  professional_summary: string;
  work_experience: Array<{
    job_title: string;
    company: string;
    location: string;
    start_date: string;
    end_date: string;
    is_current: boolean;
    achievements: string[];
  }>;
  education: Array<{
    degree: string;
    institution: string;
    location: string;
    start_date: string;
    end_date: string;
    grade?: string;
  }>;
  skills: {
    [category: string]: string[];
  };
  projects?: Array<{
    name: string;
    description: string;
    technologies: string[];
  }>;
}

interface MobilePreviewProps {
  cvData: CVData;
  onClose: () => void;
  onEdit: () => void;
  onExport: (format: string) => void;
  onShare: () => void;
  template?: string;
}

const MobilePreview: React.FC<MobilePreviewProps> = ({
  cvData,
  onClose,
  onEdit,
  onExport,
  onShare,
  template = 'modern'
}) => {
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [showActions, setShowActions] = useState(false);

  const renderModernTemplate = () => (
    <div className="bg-white min-h-full">
      {/* Header Section */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-6 text-center">
        <h1 className="text-2xl font-bold mb-2 uppercase tracking-wide">
          {cvData.personal_details.full_name || 'Your Name'}
        </h1>
        {cvData.personal_details.desired_position && (
          <p className="text-blue-100 text-lg mb-4">
            {cvData.personal_details.desired_position}
          </p>
        )}
        
        <div className="flex flex-wrap justify-center gap-4 text-sm">
          {cvData.personal_details.phone && (
            <div className="flex items-center">
              <span className="mr-2">📞</span>
              {cvData.personal_details.phone}
            </div>
          )}
          {cvData.personal_details.email && (
            <div className="flex items-center">
              <span className="mr-2">✉️</span>
              {cvData.personal_details.email}
            </div>
          )}
          {cvData.personal_details.location && (
            <div className="flex items-center">
              <span className="mr-2">📍</span>
              {cvData.personal_details.location}
            </div>
          )}
          {cvData.personal_details.linkedin_url && (
            <div className="flex items-center">
              <span className="mr-2">💼</span>
              LinkedIn
            </div>
          )}
        </div>
      </div>

      {/* Content */}
      <div className="p-6 space-y-8">
        {/* Professional Summary */}
        {cvData.professional_summary && (
          <section>
            <h2 className="text-lg font-semibold text-blue-600 border-b-2 border-blue-600 pb-2 mb-4 uppercase tracking-wide">
              Professional Summary
            </h2>
            <p className="text-gray-700 leading-relaxed text-justify">
              {cvData.professional_summary}
            </p>
          </section>
        )}

        {/* Skills */}
        {Object.keys(cvData.skills).length > 0 && (
          <section>
            <h2 className="text-lg font-semibold text-blue-600 border-b-2 border-blue-600 pb-2 mb-4 uppercase tracking-wide">
              Technical Skills
            </h2>
            <div className="space-y-4">
              {Object.entries(cvData.skills).map(([category, skills]) => (
                skills.length > 0 && (
                  <div key={category} className="bg-gray-50 p-4 rounded-lg border-l-4 border-blue-600">
                    <h3 className="font-semibold text-gray-800 mb-3 capitalize">
                      {category}
                    </h3>
                    <div className="flex flex-wrap gap-2">
                      {skills.filter(skill => skill.trim()).map((skill, index) => (
                        <span
                          key={index}
                          className="bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-medium"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                )
              ))}
            </div>
          </section>
        )}

        {/* Work Experience */}
        {cvData.work_experience.length > 0 && (
          <section>
            <h2 className="text-lg font-semibold text-blue-600 border-b-2 border-blue-600 pb-2 mb-4 uppercase tracking-wide">
              Work Experience
            </h2>
            <div className="space-y-6">
              {cvData.work_experience.map((exp, index) => (
                <div key={index} className="border-l-4 border-gray-200 pl-4 pb-4">
                  <div className="mb-2">
                    <h3 className="text-lg font-semibold text-gray-800">
                      {exp.job_title || 'Job Title'}
                    </h3>
                    <p className="text-blue-600 font-medium">
                      {exp.company || 'Company Name'}
                    </p>
                    {exp.location && (
                      <p className="text-gray-600 text-sm">{exp.location}</p>
                    )}
                  </div>
                  
                  <div className="text-gray-600 text-sm mb-3 font-medium">
                    {exp.start_date && (
                      <>
                        {exp.start_date} - {exp.is_current ? 'Present' : exp.end_date || 'Present'}
                      </>
                    )}
                  </div>

                  {exp.achievements.length > 0 && (
                    <ul className="space-y-2">
                      {exp.achievements
                        .filter(achievement => achievement.trim())
                        .map((achievement, achIndex) => (
                        <li key={achIndex} className="flex items-start">
                          <span className="text-blue-500 text-sm mr-2 mt-1">▶</span>
                          <span className="text-gray-700 text-sm leading-relaxed">
                            {achievement}
                          </span>
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Projects */}
        {cvData.projects && cvData.projects.length > 0 && (
          <section>
            <h2 className="text-lg font-semibold text-blue-600 border-b-2 border-blue-600 pb-2 mb-4 uppercase tracking-wide">
              Key Projects
            </h2>
            <div className="grid gap-4">
              {cvData.projects.map((project, index) => (
                <div key={index} className="bg-gray-50 p-4 rounded-lg border-l-4 border-blue-400">
                  <h3 className="font-semibold text-gray-800 mb-2">
                    {project.name || 'Project Name'}
                  </h3>
                  {project.description && (
                    <p className="text-gray-700 text-sm mb-3 leading-relaxed">
                      {project.description}
                    </p>
                  )}
                  {project.technologies && project.technologies.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                      {project.technologies
                        .filter(tech => tech.trim())
                        .map((tech, techIndex) => (
                        <span
                          key={techIndex}
                          className="bg-gray-200 text-gray-700 px-2 py-1 rounded text-xs"
                        >
                          {tech}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Education */}
        {cvData.education.length > 0 && (
          <section>
            <h2 className="text-lg font-semibold text-blue-600 border-b-2 border-blue-600 pb-2 mb-4 uppercase tracking-wide">
              Education
            </h2>
            <div className="space-y-4">
              {cvData.education.map((edu, index) => (
                <div key={index} className="flex justify-between items-start flex-wrap">
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-800">
                      {edu.degree || 'Degree'}
                    </h3>
                    <p className="text-blue-600 font-medium">
                      {edu.institution || 'Institution'}
                    </p>
                    {edu.location && (
                      <p className="text-gray-600 text-sm">{edu.location}</p>
                    )}
                    {edu.grade && (
                      <p className="text-gray-600 text-sm italic">{edu.grade}</p>
                    )}
                  </div>
                  <div className="text-gray-600 text-sm font-medium ml-4">
                    {edu.start_date && edu.end_date && (
                      `${edu.start_date} - ${edu.end_date}`
                    )}
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}
      </div>
    </div>
  );

  const renderMinimalTemplate = () => (
    <div className="bg-white min-h-full">
      {/* Header */}
      <div className="p-6 border-b-2 border-gray-900">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          {cvData.personal_details.full_name || 'Your Name'}
        </h1>
        {cvData.personal_details.desired_position && (
          <p className="text-xl text-gray-600 mb-4">
            {cvData.personal_details.desired_position}
          </p>
        )}
        
        <div className="text-sm text-gray-600 space-y-1">
          {cvData.personal_details.email && (
            <div>{cvData.personal_details.email}</div>
          )}
          {cvData.personal_details.phone && (
            <div>{cvData.personal_details.phone}</div>
          )}
          {cvData.personal_details.location && (
            <div>{cvData.personal_details.location}</div>
          )}
          {cvData.personal_details.linkedin_url && (
            <div>{cvData.personal_details.linkedin_url}</div>
          )}
        </div>
      </div>

      <div className="p-6 space-y-8">
        {/* Summary */}
        {cvData.professional_summary && (
          <section>
            <h2 className="text-lg font-bold text-gray-900 mb-3 uppercase">
              Summary
            </h2>
            <p className="text-gray-700">{cvData.professional_summary}</p>
          </section>
        )}

        {/* Experience */}
        {cvData.work_experience.length > 0 && (
          <section>
            <h2 className="text-lg font-bold text-gray-900 mb-4 uppercase">
              Experience
            </h2>
            {cvData.work_experience.map((exp, index) => (
              <div key={index} className="mb-6">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h3 className="font-bold text-gray-900">{exp.job_title}</h3>
                    <p className="text-gray-700">{exp.company}</p>
                  </div>
                  <div className="text-sm text-gray-600">
                    {exp.start_date} - {exp.is_current ? 'Present' : exp.end_date}
                  </div>
                </div>
                <ul className="list-disc list-inside text-gray-700 space-y-1">
                  {exp.achievements
                    .filter(ach => ach.trim())
                    .map((achievement, achIndex) => (
                    <li key={achIndex}>{achievement}</li>
                  ))}
                </ul>
              </div>
            ))}
          </section>
        )}

        {/* Education */}
        {cvData.education.length > 0 && (
          <section>
            <h2 className="text-lg font-bold text-gray-900 mb-4 uppercase">
              Education
            </h2>
            {cvData.education.map((edu, index) => (
              <div key={index} className="mb-4">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-bold text-gray-900">{edu.degree}</h3>
                    <p className="text-gray-700">{edu.institution}</p>
                  </div>
                  <div className="text-sm text-gray-600">
                    {edu.start_date} - {edu.end_date}
                  </div>
                </div>
              </div>
            ))}
          </section>
        )}

        {/* Skills */}
        {Object.keys(cvData.skills).length > 0 && (
          <section>
            <h2 className="text-lg font-bold text-gray-900 mb-4 uppercase">
              Skills
            </h2>
            {Object.entries(cvData.skills).map(([category, skills]) => (
              skills.length > 0 && (
                <div key={category} className="mb-3">
                  <strong className="text-gray-900 capitalize">{category}: </strong>
                  <span className="text-gray-700">
                    {skills.filter(skill => skill.trim()).join(', ')}
                  </span>
                </div>
              )
            ))}
          </section>
        )}
      </div>
    </div>
  );

  const renderTemplate = () => {
    switch (template) {
      case 'minimal':
        return renderMinimalTemplate();
      case 'modern':
      default:
        return renderModernTemplate();
    }
  };

  return (
    <div className={`fixed inset-0 bg-white z-50 ${isFullscreen ? '' : 'md:relative md:inset-auto'}`}>
      {/* Header */}
      <div className="bg-white border-b shadow-sm sticky top-0 z-10">
        <div className="px-4 py-3 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <button
              onClick={onClose}
              className="p-2 text-gray-600 hover:text-gray-800"
            >
              <XMarkIcon className="w-5 h-5" />
            </button>
            <h1 className="text-lg font-semibold text-gray-800">CV Preview</h1>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={() => setIsFullscreen(!isFullscreen)}
              className="p-2 text-gray-600 hover:text-gray-800 md:hidden"
            >
              <ArrowsPointingOutIcon className="w-5 h-5" />
            </button>

            <button
              onClick={() => setShowActions(!showActions)}
              className="px-3 py-1 bg-blue-500 text-white rounded-lg text-sm"
            >
              Actions
            </button>
          </div>
        </div>

        {/* Action Menu */}
        {showActions && (
          <div className="border-t bg-gray-50 px-4 py-3">
            <div className="grid grid-cols-2 gap-3">
              <button
                onClick={() => {
                  onEdit();
                  setShowActions(false);
                }}
                className="flex items-center justify-center px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm text-gray-700 hover:bg-gray-50"
              >
                <PencilIcon className="w-4 h-4 mr-2" />
                Edit
              </button>

              <button
                onClick={() => {
                  onShare();
                  setShowActions(false);
                }}
                className="flex items-center justify-center px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm text-gray-700 hover:bg-gray-50"
              >
                <ShareIcon className="w-4 h-4 mr-2" />
                Share
              </button>

              <button
                onClick={() => {
                  onExport('pdf');
                  setShowActions(false);
                }}
                className="flex items-center justify-center px-3 py-2 bg-blue-500 text-white rounded-lg text-sm hover:bg-blue-600"
              >
                <DocumentArrowDownIcon className="w-4 h-4 mr-2" />
                PDF
              </button>

              <button
                onClick={() => {
                  onExport('docx');
                  setShowActions(false);
                }}
                className="flex items-center justify-center px-3 py-2 bg-green-500 text-white rounded-lg text-sm hover:bg-green-600"
              >
                <DocumentArrowDownIcon className="w-4 h-4 mr-2" />
                DOCX
              </button>
            </div>
          </div>
        )}
      </div>

      {/* CV Content */}
      <div className="overflow-auto" style={{ height: 'calc(100vh - 120px)' }}>
        <div className="max-w-2xl mx-auto">
          {renderTemplate()}
        </div>
      </div>

      {/* Quick Actions Footer */}
      <div className="bg-white border-t px-4 py-3 sticky bottom-0">
        <div className="flex justify-center space-x-4">
          <button
            onClick={onEdit}
            className="flex items-center px-4 py-2 text-gray-600 hover:text-gray-800"
          >
            <PencilIcon className="w-4 h-4 mr-2" />
            <span className="text-sm">Edit</span>
          </button>

          <button
            onClick={() => onExport('pdf')}
            className="flex items-center px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
          >
            <DocumentArrowDownIcon className="w-4 h-4 mr-2" />
            <span className="text-sm">Download</span>
          </button>

          <button
            onClick={onShare}
            className="flex items-center px-4 py-2 text-gray-600 hover:text-gray-800"
          >
            <ShareIcon className="w-4 h-4 mr-2" />
            <span className="text-sm">Share</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default MobilePreview;