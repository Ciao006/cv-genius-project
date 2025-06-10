import React, { useState, useEffect, useRef } from 'react';
import { ChevronLeftIcon, ChevronRightIcon, PlusIcon, TrashIcon, EyeIcon, DocumentArrowDownIcon } from '@heroicons/react/24/outline';

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

interface MobileEditorProps {
  initialData?: CVData;
  onSave: (data: CVData) => void;
  onPreview: () => void;
  onExport: (format: string) => void;
}

const MobileEditor: React.FC<MobileEditorProps> = ({
  initialData,
  onSave,
  onPreview,
  onExport
}) => {
  const [cvData, setCvData] = useState<CVData>(initialData || {
    personal_details: {
      full_name: '',
      email: '',
      phone: '',
      location: '',
      linkedin_url: '',
      desired_position: ''
    },
    professional_summary: '',
    work_experience: [],
    education: [],
    skills: {},
    projects: []
  });

  const [currentSection, setCurrentSection] = useState(0);
  const [isAutoSaving, setIsAutoSaving] = useState(false);
  const [showExportMenu, setShowExportMenu] = useState(false);
  const autoSaveTimeoutRef = useRef<NodeJS.Timeout>();

  const sections = [
    { id: 'personal', title: 'Personal Info', icon: '👤' },
    { id: 'summary', title: 'Summary', icon: '📝' },
    { id: 'experience', title: 'Experience', icon: '💼' },
    { id: 'education', title: 'Education', icon: '🎓' },
    { id: 'skills', title: 'Skills', icon: '⚡' },
    { id: 'projects', title: 'Projects', icon: '🚀' }
  ];

  // Auto-save functionality
  useEffect(() => {
    if (autoSaveTimeoutRef.current) {
      clearTimeout(autoSaveTimeoutRef.current);
    }

    setIsAutoSaving(true);
    autoSaveTimeoutRef.current = setTimeout(() => {
      onSave(cvData);
      setIsAutoSaving(false);
    }, 2000);

    return () => {
      if (autoSaveTimeoutRef.current) {
        clearTimeout(autoSaveTimeoutRef.current);
      }
    };
  }, [cvData, onSave]);

  const updatePersonalDetails = (field: string, value: string) => {
    setCvData(prev => ({
      ...prev,
      personal_details: {
        ...prev.personal_details,
        [field]: value
      }
    }));
  };

  const updateProfessionalSummary = (value: string) => {
    setCvData(prev => ({
      ...prev,
      professional_summary: value
    }));
  };

  const addWorkExperience = () => {
    setCvData(prev => ({
      ...prev,
      work_experience: [
        ...prev.work_experience,
        {
          job_title: '',
          company: '',
          location: '',
          start_date: '',
          end_date: '',
          is_current: false,
          achievements: ['']
        }
      ]
    }));
  };

  const updateWorkExperience = (index: number, field: string, value: any) => {
    setCvData(prev => ({
      ...prev,
      work_experience: prev.work_experience.map((exp, i) => 
        i === index ? { ...exp, [field]: value } : exp
      )
    }));
  };

  const removeWorkExperience = (index: number) => {
    setCvData(prev => ({
      ...prev,
      work_experience: prev.work_experience.filter((_, i) => i !== index)
    }));
  };

  const addAchievement = (expIndex: number) => {
    setCvData(prev => ({
      ...prev,
      work_experience: prev.work_experience.map((exp, i) => 
        i === expIndex ? {
          ...exp,
          achievements: [...exp.achievements, '']
        } : exp
      )
    }));
  };

  const updateAchievement = (expIndex: number, achIndex: number, value: string) => {
    setCvData(prev => ({
      ...prev,
      work_experience: prev.work_experience.map((exp, i) => 
        i === expIndex ? {
          ...exp,
          achievements: exp.achievements.map((ach, j) => 
            j === achIndex ? value : ach
          )
        } : exp
      )
    }));
  };

  const removeAchievement = (expIndex: number, achIndex: number) => {
    setCvData(prev => ({
      ...prev,
      work_experience: prev.work_experience.map((exp, i) => 
        i === expIndex ? {
          ...exp,
          achievements: exp.achievements.filter((_, j) => j !== achIndex)
        } : exp
      )
    }));
  };

  const addEducation = () => {
    setCvData(prev => ({
      ...prev,
      education: [
        ...prev.education,
        {
          degree: '',
          institution: '',
          location: '',
          start_date: '',
          end_date: '',
          grade: ''
        }
      ]
    }));
  };

  const updateEducation = (index: number, field: string, value: string) => {
    setCvData(prev => ({
      ...prev,
      education: prev.education.map((edu, i) => 
        i === index ? { ...edu, [field]: value } : edu
      )
    }));
  };

  const removeEducation = (index: number) => {
    setCvData(prev => ({
      ...prev,
      education: prev.education.filter((_, i) => i !== index)
    }));
  };

  const addSkillCategory = () => {
    const categoryName = prompt('Enter skill category name:');
    if (categoryName) {
      setCvData(prev => ({
        ...prev,
        skills: {
          ...prev.skills,
          [categoryName]: []
        }
      }));
    }
  };

  const addSkill = (category: string) => {
    setCvData(prev => ({
      ...prev,
      skills: {
        ...prev.skills,
        [category]: [...(prev.skills[category] || []), '']
      }
    }));
  };

  const updateSkill = (category: string, index: number, value: string) => {
    setCvData(prev => ({
      ...prev,
      skills: {
        ...prev.skills,
        [category]: prev.skills[category].map((skill, i) => 
          i === index ? value : skill
        )
      }
    }));
  };

  const removeSkill = (category: string, index: number) => {
    setCvData(prev => ({
      ...prev,
      skills: {
        ...prev.skills,
        [category]: prev.skills[category].filter((_, i) => i !== index)
      }
    }));
  };

  const removeSkillCategory = (category: string) => {
    setCvData(prev => {
      const newSkills = { ...prev.skills };
      delete newSkills[category];
      return {
        ...prev,
        skills: newSkills
      };
    });
  };

  const addProject = () => {
    setCvData(prev => ({
      ...prev,
      projects: [
        ...(prev.projects || []),
        {
          name: '',
          description: '',
          technologies: ['']
        }
      ]
    }));
  };

  const updateProject = (index: number, field: string, value: any) => {
    setCvData(prev => ({
      ...prev,
      projects: (prev.projects || []).map((project, i) => 
        i === index ? { ...project, [field]: value } : project
      )
    }));
  };

  const removeProject = (index: number) => {
    setCvData(prev => ({
      ...prev,
      projects: (prev.projects || []).filter((_, i) => i !== index)
    }));
  };

  const addTechnology = (projectIndex: number) => {
    setCvData(prev => ({
      ...prev,
      projects: (prev.projects || []).map((project, i) => 
        i === projectIndex ? {
          ...project,
          technologies: [...project.technologies, '']
        } : project
      )
    }));
  };

  const updateTechnology = (projectIndex: number, techIndex: number, value: string) => {
    setCvData(prev => ({
      ...prev,
      projects: (prev.projects || []).map((project, i) => 
        i === projectIndex ? {
          ...project,
          technologies: project.technologies.map((tech, j) => 
            j === techIndex ? value : tech
          )
        } : project
      )
    }));
  };

  const removeTechnology = (projectIndex: number, techIndex: number) => {
    setCvData(prev => ({
      ...prev,
      projects: (prev.projects || []).map((project, i) => 
        i === projectIndex ? {
          ...project,
          technologies: project.technologies.filter((_, j) => j !== techIndex)
        } : project
      )
    }));
  };

  const nextSection = () => {
    if (currentSection < sections.length - 1) {
      setCurrentSection(currentSection + 1);
    }
  };

  const previousSection = () => {
    if (currentSection > 0) {
      setCurrentSection(currentSection - 1);
    }
  };

  const renderPersonalDetails = () => (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Personal Information</h2>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
        <input
          type="text"
          value={cvData.personal_details.full_name}
          onChange={(e) => updatePersonalDetails('full_name', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Enter your full name"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
        <input
          type="email"
          value={cvData.personal_details.email}
          onChange={(e) => updatePersonalDetails('email', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="your.email@example.com"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
        <input
          type="tel"
          value={cvData.personal_details.phone}
          onChange={(e) => updatePersonalDetails('phone', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="+1 (555) 123-4567"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
        <input
          type="text"
          value={cvData.personal_details.location}
          onChange={(e) => updatePersonalDetails('location', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="City, State, Country"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">LinkedIn URL</label>
        <input
          type="url"
          value={cvData.personal_details.linkedin_url}
          onChange={(e) => updatePersonalDetails('linkedin_url', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="https://linkedin.com/in/yourprofile"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Desired Position</label>
        <input
          type="text"
          value={cvData.personal_details.desired_position}
          onChange={(e) => updatePersonalDetails('desired_position', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Software Engineer"
        />
      </div>
    </div>
  );

  const renderProfessionalSummary = () => (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Professional Summary</h2>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Summary
          <span className="text-xs text-gray-500 ml-2">(2-3 sentences highlighting your key strengths)</span>
        </label>
        <textarea
          value={cvData.professional_summary}
          onChange={(e) => updateProfessionalSummary(e.target.value)}
          rows={4}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
          placeholder="Write a compelling summary of your professional background, key skills, and career objectives..."
        />
        <div className="text-xs text-gray-500 mt-1">
          {cvData.professional_summary.length}/400 characters
        </div>
      </div>
    </div>
  );

  const renderWorkExperience = () => (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold text-gray-800">Work Experience</h2>
        <button
          onClick={addWorkExperience}
          className="flex items-center px-3 py-1 bg-blue-500 text-white rounded-lg text-sm"
        >
          <PlusIcon className="w-4 h-4 mr-1" />
          Add
        </button>
      </div>

      {cvData.work_experience.map((exp, expIndex) => (
        <div key={expIndex} className="border border-gray-200 rounded-lg p-4 space-y-3">
          <div className="flex justify-between items-start">
            <h3 className="font-medium text-gray-800">Experience #{expIndex + 1}</h3>
            <button
              onClick={() => removeWorkExperience(expIndex)}
              className="text-red-500 hover:text-red-700"
            >
              <TrashIcon className="w-4 h-4" />
            </button>
          </div>

          <div className="grid grid-cols-1 gap-3">
            <input
              type="text"
              value={exp.job_title}
              onChange={(e) => updateWorkExperience(expIndex, 'job_title', e.target.value)}
              placeholder="Job Title"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />

            <input
              type="text"
              value={exp.company}
              onChange={(e) => updateWorkExperience(expIndex, 'company', e.target.value)}
              placeholder="Company Name"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />

            <input
              type="text"
              value={exp.location}
              onChange={(e) => updateWorkExperience(expIndex, 'location', e.target.value)}
              placeholder="Location"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />

            <div className="grid grid-cols-2 gap-2">
              <input
                type="text"
                value={exp.start_date}
                onChange={(e) => updateWorkExperience(expIndex, 'start_date', e.target.value)}
                placeholder="Start Date (MM/YYYY)"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />

              <input
                type="text"
                value={exp.end_date}
                onChange={(e) => updateWorkExperience(expIndex, 'end_date', e.target.value)}
                placeholder="End Date (MM/YYYY)"
                disabled={exp.is_current}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
              />
            </div>

            <label className="flex items-center">
              <input
                type="checkbox"
                checked={exp.is_current}
                onChange={(e) => {
                  updateWorkExperience(expIndex, 'is_current', e.target.checked);
                  if (e.target.checked) {
                    updateWorkExperience(expIndex, 'end_date', '');
                  }
                }}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span className="ml-2 text-sm text-gray-700">Currently working here</span>
            </label>
          </div>

          <div>
            <div className="flex justify-between items-center mb-2">
              <label className="text-sm font-medium text-gray-700">Achievements</label>
              <button
                onClick={() => addAchievement(expIndex)}
                className="text-blue-500 text-sm"
              >
                + Add Achievement
              </button>
            </div>

            {exp.achievements.map((achievement, achIndex) => (
              <div key={achIndex} className="flex items-start space-x-2 mb-2">
                <span className="text-gray-400 mt-2">•</span>
                <textarea
                  value={achievement}
                  onChange={(e) => updateAchievement(expIndex, achIndex, e.target.value)}
                  placeholder="Describe a key achievement or responsibility..."
                  rows={2}
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none text-sm"
                />
                <button
                  onClick={() => removeAchievement(expIndex, achIndex)}
                  className="text-red-500 hover:text-red-700 mt-2"
                >
                  <TrashIcon className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        </div>
      ))}

      {cvData.work_experience.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          <p>No work experience added yet.</p>
          <button
            onClick={addWorkExperience}
            className="mt-2 text-blue-500 hover:text-blue-700"
          >
            Add your first work experience
          </button>
        </div>
      )}
    </div>
  );

  const renderEducation = () => (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold text-gray-800">Education</h2>
        <button
          onClick={addEducation}
          className="flex items-center px-3 py-1 bg-blue-500 text-white rounded-lg text-sm"
        >
          <PlusIcon className="w-4 h-4 mr-1" />
          Add
        </button>
      </div>

      {cvData.education.map((edu, index) => (
        <div key={index} className="border border-gray-200 rounded-lg p-4 space-y-3">
          <div className="flex justify-between items-start">
            <h3 className="font-medium text-gray-800">Education #{index + 1}</h3>
            <button
              onClick={() => removeEducation(index)}
              className="text-red-500 hover:text-red-700"
            >
              <TrashIcon className="w-4 h-4" />
            </button>
          </div>

          <div className="space-y-3">
            <input
              type="text"
              value={edu.degree}
              onChange={(e) => updateEducation(index, 'degree', e.target.value)}
              placeholder="Degree (e.g., Bachelor of Science in Computer Science)"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />

            <input
              type="text"
              value={edu.institution}
              onChange={(e) => updateEducation(index, 'institution', e.target.value)}
              placeholder="Institution Name"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />

            <input
              type="text"
              value={edu.location}
              onChange={(e) => updateEducation(index, 'location', e.target.value)}
              placeholder="Location"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />

            <div className="grid grid-cols-2 gap-2">
              <input
                type="text"
                value={edu.start_date}
                onChange={(e) => updateEducation(index, 'start_date', e.target.value)}
                placeholder="Start Date"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />

              <input
                type="text"
                value={edu.end_date}
                onChange={(e) => updateEducation(index, 'end_date', e.target.value)}
                placeholder="End Date"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <input
              type="text"
              value={edu.grade || ''}
              onChange={(e) => updateEducation(index, 'grade', e.target.value)}
              placeholder="Grade/GPA (optional)"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>
      ))}

      {cvData.education.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          <p>No education added yet.</p>
          <button
            onClick={addEducation}
            className="mt-2 text-blue-500 hover:text-blue-700"
          >
            Add your education
          </button>
        </div>
      )}
    </div>
  );

  const renderSkills = () => (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold text-gray-800">Skills</h2>
        <button
          onClick={addSkillCategory}
          className="flex items-center px-3 py-1 bg-blue-500 text-white rounded-lg text-sm"
        >
          <PlusIcon className="w-4 h-4 mr-1" />
          Category
        </button>
      </div>

      {Object.entries(cvData.skills).map(([category, skills]) => (
        <div key={category} className="border border-gray-200 rounded-lg p-4 space-y-3">
          <div className="flex justify-between items-center">
            <h3 className="font-medium text-gray-800 capitalize">{category}</h3>
            <button
              onClick={() => removeSkillCategory(category)}
              className="text-red-500 hover:text-red-700"
            >
              <TrashIcon className="w-4 h-4" />
            </button>
          </div>

          <div className="space-y-2">
            {skills.map((skill, index) => (
              <div key={index} className="flex items-center space-x-2">
                <input
                  type="text"
                  value={skill}
                  onChange={(e) => updateSkill(category, index, e.target.value)}
                  placeholder="Enter skill"
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <button
                  onClick={() => removeSkill(category, index)}
                  className="text-red-500 hover:text-red-700"
                >
                  <TrashIcon className="w-4 h-4" />
                </button>
              </div>
            ))}

            <button
              onClick={() => addSkill(category)}
              className="w-full py-2 border-2 border-dashed border-gray-300 rounded-lg text-gray-500 hover:border-blue-300 hover:text-blue-500"
            >
              + Add Skill
            </button>
          </div>
        </div>
      ))}

      {Object.keys(cvData.skills).length === 0 && (
        <div className="text-center py-8 text-gray-500">
          <p>No skill categories added yet.</p>
          <button
            onClick={addSkillCategory}
            className="mt-2 text-blue-500 hover:text-blue-700"
          >
            Add your first skill category
          </button>
        </div>
      )}
    </div>
  );

  const renderProjects = () => (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold text-gray-800">Projects</h2>
        <button
          onClick={addProject}
          className="flex items-center px-3 py-1 bg-blue-500 text-white rounded-lg text-sm"
        >
          <PlusIcon className="w-4 h-4 mr-1" />
          Add
        </button>
      </div>

      {(cvData.projects || []).map((project, index) => (
        <div key={index} className="border border-gray-200 rounded-lg p-4 space-y-3">
          <div className="flex justify-between items-start">
            <h3 className="font-medium text-gray-800">Project #{index + 1}</h3>
            <button
              onClick={() => removeProject(index)}
              className="text-red-500 hover:text-red-700"
            >
              <TrashIcon className="w-4 h-4" />
            </button>
          </div>

          <div className="space-y-3">
            <input
              type="text"
              value={project.name}
              onChange={(e) => updateProject(index, 'name', e.target.value)}
              placeholder="Project Name"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />

            <textarea
              value={project.description}
              onChange={(e) => updateProject(index, 'description', e.target.value)}
              placeholder="Project description..."
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            />

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Technologies</label>
              {project.technologies.map((tech, techIndex) => (
                <div key={techIndex} className="flex items-center space-x-2 mb-2">
                  <input
                    type="text"
                    value={tech}
                    onChange={(e) => updateTechnology(index, techIndex, e.target.value)}
                    placeholder="Technology/Tool"
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  <button
                    onClick={() => removeTechnology(index, techIndex)}
                    className="text-red-500 hover:text-red-700"
                  >
                    <TrashIcon className="w-4 h-4" />
                  </button>
                </div>
              ))}

              <button
                onClick={() => addTechnology(index)}
                className="w-full py-2 border-2 border-dashed border-gray-300 rounded-lg text-gray-500 hover:border-blue-300 hover:text-blue-500"
              >
                + Add Technology
              </button>
            </div>
          </div>
        </div>
      ))}

      {(cvData.projects || []).length === 0 && (
        <div className="text-center py-8 text-gray-500">
          <p>No projects added yet.</p>
          <button
            onClick={addProject}
            className="mt-2 text-blue-500 hover:text-blue-700"
          >
            Add your first project
          </button>
        </div>
      )}
    </div>
  );

  const renderSection = () => {
    switch (sections[currentSection].id) {
      case 'personal':
        return renderPersonalDetails();
      case 'summary':
        return renderProfessionalSummary();
      case 'experience':
        return renderWorkExperience();
      case 'education':
        return renderEducation();
      case 'skills':
        return renderSkills();
      case 'projects':
        return renderProjects();
      default:
        return renderPersonalDetails();
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b sticky top-0 z-10">
        <div className="px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <h1 className="text-lg font-semibold text-gray-800">CV Editor</h1>
              {isAutoSaving && (
                <span className="text-xs text-blue-500 flex items-center">
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse mr-1"></div>
                  Saving...
                </span>
              )}
            </div>
            <div className="flex items-center space-x-2">
              <button
                onClick={onPreview}
                className="p-2 text-gray-600 hover:text-gray-800"
              >
                <EyeIcon className="w-5 h-5" />
              </button>
              <div className="relative">
                <button
                  onClick={() => setShowExportMenu(!showExportMenu)}
                  className="p-2 text-gray-600 hover:text-gray-800"
                >
                  <DocumentArrowDownIcon className="w-5 h-5" />
                </button>
                {showExportMenu && (
                  <div className="absolute right-0 top-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg py-1 z-20">
                    <button
                      onClick={() => {
                        onExport('pdf');
                        setShowExportMenu(false);
                      }}
                      className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    >
                      Export PDF
                    </button>
                    <button
                      onClick={() => {
                        onExport('docx');
                        setShowExportMenu(false);
                      }}
                      className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    >
                      Export DOCX
                    </button>
                    <button
                      onClick={() => {
                        onExport('txt');
                        setShowExportMenu(false);
                      }}
                      className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    >
                      Export TXT
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Section Navigation */}
      <div className="bg-white border-b">
        <div className="px-4 py-2">
          <div className="flex items-center justify-between">
            <button
              onClick={previousSection}
              disabled={currentSection === 0}
              className="p-2 text-gray-400 disabled:opacity-50"
            >
              <ChevronLeftIcon className="w-5 h-5" />
            </button>

            <div className="flex-1 mx-4">
              <div className="text-center">
                <div className="text-sm font-medium text-gray-800 flex items-center justify-center">
                  <span className="mr-2">{sections[currentSection].icon}</span>
                  {sections[currentSection].title}
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  {currentSection + 1} of {sections.length}
                </div>
              </div>
              
              {/* Progress bar */}
              <div className="w-full bg-gray-200 rounded-full h-1 mt-2">
                <div
                  className="bg-blue-500 h-1 rounded-full transition-all duration-300"
                  style={{ width: `${((currentSection + 1) / sections.length) * 100}%` }}
                ></div>
              </div>
            </div>

            <button
              onClick={nextSection}
              disabled={currentSection === sections.length - 1}
              className="p-2 text-gray-400 disabled:opacity-50"
            >
              <ChevronRightIcon className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Section Content */}
      <div className="px-4 py-6">
        {renderSection()}
      </div>

      {/* Bottom Navigation */}
      <div className="bg-white border-t px-4 py-3 sticky bottom-0">
        <div className="flex justify-between items-center">
          <button
            onClick={previousSection}
            disabled={currentSection === 0}
            className="px-4 py-2 text-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>

          <div className="flex space-x-2">
            {sections.map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentSection(index)}
                className={`w-3 h-3 rounded-full ${
                  index === currentSection
                    ? 'bg-blue-500'
                    : index < currentSection
                    ? 'bg-green-500'
                    : 'bg-gray-300'
                }`}
              />
            ))}
          </div>

          <button
            onClick={nextSection}
            disabled={currentSection === sections.length - 1}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {currentSection === sections.length - 1 ? 'Done' : 'Next'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default MobileEditor;