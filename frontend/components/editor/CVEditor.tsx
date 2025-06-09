import React, { useState, useEffect } from 'react';
import { Eye, Download, RotateCcw, Save, Edit3, User, Briefcase, GraduationCap, Award } from 'lucide-react';
import { toast } from 'react-hot-toast';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import Textarea from '@/components/ui/Textarea';
import { cvAPI, downloadPDF, getErrorMessage } from '@/utils/api';

interface CVData {
  personal_details: {
    full_name: string;
    email: string;
    phone: string;
    linkedin_url?: string;
    location: string;
    github_url?: string;
    website_url?: string;
  };
  professional_summary: string;
  work_experience: Array<{
    job_title: string;
    company: string;
    start_date: string;
    end_date?: string;
    is_current: boolean;
    location?: string;
    achievements: string[];
  }>;
  education: Array<{
    degree: string;
    institution: string;
    start_date: string;
    end_date?: string;
    grade?: string;
    location?: string;
  }>;
  skills: {
    technical: string[];
    soft: string[];
    languages: string[];
  };
  generation_date?: string;
}

interface CVEditorProps {
  initialData: CVData;
  onSave?: (data: CVData) => void;
  onRegenerate?: () => void;
}

const CVEditor: React.FC<CVEditorProps> = ({
  initialData,
  onSave,
  onRegenerate
}) => {
  const [cvData, setCvData] = useState<CVData>(initialData);
  const [isPreviewMode, setIsPreviewMode] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const [activeSection, setActiveSection] = useState<string>('personal');

  useEffect(() => {
    setCvData(initialData);
  }, [initialData]);

  const handleSaveChanges = async () => {
    try {
      setIsGenerating(true);
      
      // Generate new CV PDF with updated data
      const response = await cvAPI.generateCVPDF(cvData);
      
      // Download the updated CV
      downloadPDF(response.cv_pdf_base64, response.filename_cv);
      
      toast.success('CV updated and downloaded successfully!');
      if (onSave) {
        onSave(cvData);
      }
    } catch (error) {
      const message = getErrorMessage(error);
      toast.error(`Failed to generate PDF: ${message}`);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleDownloadOriginal = () => {
    // This would download the original PDF from session storage or props
    toast.success('Original CV download would be implemented here');
  };

  const renderPersonalSection = () => (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input
          label="Full Name"
          value={cvData.personal_details.full_name}
          onChange={(e) => setCvData(prev => ({
            ...prev,
            personal_details: { ...prev.personal_details, full_name: e.target.value }
          }))}
          disabled={isPreviewMode}
        />
        <Input
          label="Email"
          type="email"
          value={cvData.personal_details.email}
          onChange={(e) => setCvData(prev => ({
            ...prev,
            personal_details: { ...prev.personal_details, email: e.target.value }
          }))}
          disabled={isPreviewMode}
        />
        <Input
          label="Phone"
          value={cvData.personal_details.phone}
          onChange={(e) => setCvData(prev => ({
            ...prev,
            personal_details: { ...prev.personal_details, phone: e.target.value }
          }))}
          disabled={isPreviewMode}
        />
        <Input
          label="Location"
          value={cvData.personal_details.location}
          onChange={(e) => setCvData(prev => ({
            ...prev,
            personal_details: { ...prev.personal_details, location: e.target.value }
          }))}
          disabled={isPreviewMode}
        />
        {cvData.personal_details.linkedin_url && (
          <Input
            label="LinkedIn URL"
            value={cvData.personal_details.linkedin_url}
            onChange={(e) => setCvData(prev => ({
              ...prev,
              personal_details: { ...prev.personal_details, linkedin_url: e.target.value }
            }))}
            disabled={isPreviewMode}
          />
        )}
        {cvData.personal_details.github_url && (
          <Input
            label="GitHub URL"
            value={cvData.personal_details.github_url}
            onChange={(e) => setCvData(prev => ({
              ...prev,
              personal_details: { ...prev.personal_details, github_url: e.target.value }
            }))}
            disabled={isPreviewMode}
          />
        )}
      </div>
      <Textarea
        label="Professional Summary"
        value={cvData.professional_summary}
        onChange={(e) => setCvData(prev => ({
          ...prev,
          professional_summary: e.target.value
        }))}
        disabled={isPreviewMode}
        rows={4}
      />
    </div>
  );

  const renderWorkExperience = () => (
    <div className="space-y-6">
      {cvData.work_experience.map((exp, index) => (
        <div key={index} className="p-4 border border-gray-200 rounded-lg">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <Input
              label="Job Title"
              value={exp.job_title}
              onChange={(e) => {
                const newExp = [...cvData.work_experience];
                newExp[index] = { ...exp, job_title: e.target.value };
                setCvData(prev => ({ ...prev, work_experience: newExp }));
              }}
              disabled={isPreviewMode}
            />
            <Input
              label="Company"
              value={exp.company}
              onChange={(e) => {
                const newExp = [...cvData.work_experience];
                newExp[index] = { ...exp, company: e.target.value };
                setCvData(prev => ({ ...prev, work_experience: newExp }));
              }}
              disabled={isPreviewMode}
            />
            <Input
              label="Start Date"
              value={exp.start_date}
              onChange={(e) => {
                const newExp = [...cvData.work_experience];
                newExp[index] = { ...exp, start_date: e.target.value };
                setCvData(prev => ({ ...prev, work_experience: newExp }));
              }}
              disabled={isPreviewMode}
            />
            <Input
              label="End Date"
              value={exp.end_date || ''}
              onChange={(e) => {
                const newExp = [...cvData.work_experience];
                newExp[index] = { ...exp, end_date: e.target.value };
                setCvData(prev => ({ ...prev, work_experience: newExp }));
              }}
              disabled={isPreviewMode}
              placeholder={exp.is_current ? 'Present' : 'End date'}
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-700">Achievements</label>
            {exp.achievements.map((achievement, achIndex) => (
              <Textarea
                key={achIndex}
                value={achievement}
                onChange={(e) => {
                  const newExp = [...cvData.work_experience];
                  newExp[index].achievements[achIndex] = e.target.value;
                  setCvData(prev => ({ ...prev, work_experience: newExp }));
                }}
                disabled={isPreviewMode}
                rows={2}
                placeholder={`Achievement ${achIndex + 1}`}
              />
            ))}
          </div>
        </div>
      ))}
    </div>
  );

  const renderEducation = () => (
    <div className="space-y-6">
      {cvData.education.map((edu, index) => (
        <div key={index} className="p-4 border border-gray-200 rounded-lg">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Degree"
              value={edu.degree}
              onChange={(e) => {
                const newEdu = [...cvData.education];
                newEdu[index] = { ...edu, degree: e.target.value };
                setCvData(prev => ({ ...prev, education: newEdu }));
              }}
              disabled={isPreviewMode}
            />
            <Input
              label="Institution"
              value={edu.institution}
              onChange={(e) => {
                const newEdu = [...cvData.education];
                newEdu[index] = { ...edu, institution: e.target.value };
                setCvData(prev => ({ ...prev, education: newEdu }));
              }}
              disabled={isPreviewMode}
            />
            <Input
              label="Start Date"
              value={edu.start_date}
              onChange={(e) => {
                const newEdu = [...cvData.education];
                newEdu[index] = { ...edu, start_date: e.target.value };
                setCvData(prev => ({ ...prev, education: newEdu }));
              }}
              disabled={isPreviewMode}
            />
            <Input
              label="End Date"
              value={edu.end_date || ''}
              onChange={(e) => {
                const newEdu = [...cvData.education];
                newEdu[index] = { ...edu, end_date: e.target.value };
                setCvData(prev => ({ ...prev, education: newEdu }));
              }}
              disabled={isPreviewMode}
            />
            {edu.grade && (
              <Input
                label="Grade"
                value={edu.grade}
                onChange={(e) => {
                  const newEdu = [...cvData.education];
                  newEdu[index] = { ...edu, grade: e.target.value };
                  setCvData(prev => ({ ...prev, education: newEdu }));
                }}
                disabled={isPreviewMode}
              />
            )}
          </div>
        </div>
      ))}
    </div>
  );

  const renderSkills = () => (
    <div className="space-y-4">
      <Textarea
        label="Technical Skills"
        value={cvData.skills.technical.join(', ')}
        onChange={(e) => setCvData(prev => ({
          ...prev,
          skills: { ...prev.skills, technical: e.target.value.split(', ').filter(s => s.trim()) }
        }))}
        disabled={isPreviewMode}
        rows={3}
      />
      <Textarea
        label="Soft Skills"
        value={cvData.skills.soft.join(', ')}
        onChange={(e) => setCvData(prev => ({
          ...prev,
          skills: { ...prev.skills, soft: e.target.value.split(', ').filter(s => s.trim()) }
        }))}
        disabled={isPreviewMode}
        rows={3}
      />
      <Textarea
        label="Languages"
        value={cvData.skills.languages.join(', ')}
        onChange={(e) => setCvData(prev => ({
          ...prev,
          skills: { ...prev.skills, languages: e.target.value.split(', ').filter(s => s.trim()) }
        }))}
        disabled={isPreviewMode}
        rows={2}
      />
    </div>
  );

  const sectionButtons = [
    { id: 'personal', label: 'Personal', icon: <User className="w-4 h-4" /> },
    { id: 'experience', label: 'Experience', icon: <Briefcase className="w-4 h-4" /> },
    { id: 'education', label: 'Education', icon: <GraduationCap className="w-4 h-4" /> },
    { id: 'skills', label: 'Skills', icon: <Award className="w-4 h-4" /> },
  ];

  const renderActiveSection = () => {
    switch (activeSection) {
      case 'personal':
        return renderPersonalSection();
      case 'experience':
        return renderWorkExperience();
      case 'education':
        return renderEducation();
      case 'skills':
        return renderSkills();
      default:
        return renderPersonalSection();
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-6 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">CV Preview & Editor</h2>
            <p className="text-gray-600">Review and edit your CV content before downloading</p>
          </div>
          <div className="flex items-center gap-3">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setIsPreviewMode(!isPreviewMode)}
              icon={isPreviewMode ? <Edit3 className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
            >
              {isPreviewMode ? 'Edit' : 'Preview'}
            </Button>
          </div>
        </div>
      </div>

      {/* Section Navigation */}
      <div className="flex border-b border-gray-200 bg-gray-50">
        {sectionButtons.map((section) => (
          <button
            key={section.id}
            onClick={() => setActiveSection(section.id)}
            className={`flex items-center gap-2 px-6 py-3 text-sm font-medium transition-colors ${
              activeSection === section.id
                ? 'text-blue-600 border-b-2 border-blue-600 bg-white'
                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
            }`}
          >
            {section.icon}
            {section.label}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="p-8">
        {renderActiveSection()}
      </div>

      {/* Actions */}
      <div className="p-6 bg-gray-50 border-t border-gray-200">
        <div className="flex flex-col sm:flex-row gap-4 justify-between">
          <div className="flex gap-3">
            <Button
              variant="outline"
              onClick={handleDownloadOriginal}
              icon={<Download className="w-4 h-4" />}
              size="sm"
            >
              Download Original
            </Button>
            {onRegenerate && (
              <Button
                variant="outline"
                onClick={onRegenerate}
                icon={<RotateCcw className="w-4 h-4" />}
                size="sm"
              >
                Regenerate with AI
              </Button>
            )}
          </div>
          
          <Button
            onClick={handleSaveChanges}
            loading={isGenerating}
            disabled={isGenerating || isPreviewMode}
            icon={<Save className="w-4 h-4" />}
            className="bg-green-600 hover:bg-green-700"
          >
            {isGenerating ? 'Generating PDF...' : 'Save Changes & Download'}
          </Button>
        </div>
      </div>
    </div>
  );
};

export default CVEditor;