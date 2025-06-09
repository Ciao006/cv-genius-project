import React, { useState, useEffect } from 'react';
import Button from '@/components/ui/Button';
import LoadingSpinner from '@/components/ui/LoadingSpinner';

export interface CoverLetterData {
  personal_details: {
    full_name: string;
    email: string;
    phone: string;
    linkedin_url?: string;
    location: string;
  };
  company_name: string;
  company_address?: string;
  job_title: string;
  cover_letter_body: string;
  generation_date: string;
  include_company_address?: boolean;
}

interface CoverLetterEditorProps {
  initialData: CoverLetterData;
  onSave: (data: CoverLetterData) => void;
  onCancel: () => void;
  onRegenerate: () => void;
  isRegenerating?: boolean;
}

export const CoverLetterEditor: React.FC<CoverLetterEditorProps> = ({
  initialData,
  onSave,
  onCancel,
  onRegenerate,
  isRegenerating = false,
}) => {
  const [editableData, setEditableData] = useState<CoverLetterData>({
    ...initialData,
    include_company_address: false,
    company_address: ''
  });
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    setEditableData(initialData);
  }, [initialData]);

  const handleInputChange = (field: keyof CoverLetterData, value: string) => {
    setEditableData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handlePersonalDetailChange = (field: keyof CoverLetterData['personal_details'], value: string) => {
    setEditableData(prev => ({
      ...prev,
      personal_details: {
        ...prev.personal_details,
        [field]: value
      }
    }));
  };

  const handleSave = () => {
    onSave(editableData);
    setIsEditing(false);
  };

  const handleCancel = () => {
    if (isEditing) {
      setEditableData(initialData);
      setIsEditing(false);
    } else {
      onCancel();
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Cover Letter Preview & Editor</h2>
        <div className="flex gap-3">
          <Button
            variant="outline"
            onClick={onRegenerate}
            disabled={isRegenerating}
            className="flex items-center gap-2"
          >
            {isRegenerating ? <LoadingSpinner size="sm" /> : null}
            Regenerate with AI
          </Button>
          <Button
            variant="outline"
            onClick={() => setIsEditing(!isEditing)}
            className={isEditing ? 'bg-blue-50 border-blue-300' : ''}
          >
            {isEditing ? 'Preview Mode' : 'Edit Mode'}
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Editor Panel */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-800">
            {isEditing ? 'Edit Cover Letter' : 'Cover Letter Details'}
          </h3>
          
          {/* Personal Details */}
          <div className="space-y-3 p-4 bg-gray-50 rounded-lg">
            <h4 className="font-medium text-gray-700">Personal Details</h4>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div>
                <label className="block text-sm font-medium text-gray-600 mb-1">Full Name</label>
                {isEditing ? (
                  <input
                    type="text"
                    value={editableData.personal_details.full_name}
                    onChange={(e) => handlePersonalDetailChange('full_name', e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                ) : (
                  <p className="p-2 bg-white rounded border">{editableData.personal_details.full_name}</p>
                )}
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-600 mb-1">Email</label>
                {isEditing ? (
                  <input
                    type="email"
                    value={editableData.personal_details.email}
                    onChange={(e) => handlePersonalDetailChange('email', e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                ) : (
                  <p className="p-2 bg-white rounded border">{editableData.personal_details.email}</p>
                )}
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-600 mb-1">Phone</label>
                {isEditing ? (
                  <input
                    type="tel"
                    value={editableData.personal_details.phone}
                    onChange={(e) => handlePersonalDetailChange('phone', e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                ) : (
                  <p className="p-2 bg-white rounded border">{editableData.personal_details.phone}</p>
                )}
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-600 mb-1">Location</label>
                {isEditing ? (
                  <input
                    type="text"
                    value={editableData.personal_details.location}
                    onChange={(e) => handlePersonalDetailChange('location', e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                ) : (
                  <p className="p-2 bg-white rounded border">{editableData.personal_details.location}</p>
                )}
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-600 mb-1">LinkedIn URL</label>
              {isEditing ? (
                <input
                  type="url"
                  value={editableData.personal_details.linkedin_url || ''}
                  onChange={(e) => handlePersonalDetailChange('linkedin_url', e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              ) : (
                <p className="p-2 bg-white rounded border">{editableData.personal_details.linkedin_url || 'Not provided'}</p>
              )}
            </div>
          </div>

          {/* Company Details */}
          <div className="space-y-3 p-4 bg-gray-50 rounded-lg">
            <h4 className="font-medium text-gray-700">Company & Position</h4>
            
            <div>
              <label className="block text-sm font-medium text-gray-600 mb-1">Company Name</label>
              {isEditing ? (
                <input
                  type="text"
                  value={editableData.company_name}
                  onChange={(e) => handleInputChange('company_name', e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              ) : (
                <p className="p-2 bg-white rounded border">{editableData.company_name}</p>
              )}
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-600 mb-1">Job Title</label>
              {isEditing ? (
                <input
                  type="text"
                  value={editableData.job_title}
                  onChange={(e) => handleInputChange('job_title', e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              ) : (
                <p className="p-2 bg-white rounded border">{editableData.job_title}</p>
              )}
            </div>
            
            {/* Company Address Toggle */}
            <div className="mt-4">
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={editableData.include_company_address || false}
                  onChange={(e) => {
                    setEditableData(prev => ({
                      ...prev,
                      include_company_address: e.target.checked,
                      company_address: e.target.checked ? prev.company_address : ''
                    }));
                  }}
                  className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                  disabled={!isEditing}
                />
                <span className="text-sm font-medium text-gray-600">Include Company Address</span>
              </label>
            </div>
            
            {/* Company Address Input */}
            {editableData.include_company_address && (
              <div className="mt-3">
                <label className="block text-sm font-medium text-gray-600 mb-1">Company Address</label>
                {isEditing ? (
                  <textarea
                    value={editableData.company_address || ''}
                    onChange={(e) => handleInputChange('company_address', e.target.value)}
                    rows={3}
                    className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Enter company address...\ne.g., 123 Business Street\nDublin 2, Ireland"
                  />
                ) : (
                  <p className="p-2 bg-white rounded border min-h-[80px] whitespace-pre-wrap">
                    {editableData.company_address || 'Not provided'}
                  </p>
                )}
              </div>
            )}
          </div>

          {/* Cover Letter Body */}
          <div className="space-y-3">
            <label className="block text-sm font-medium text-gray-600">Cover Letter Content</label>
            {isEditing ? (
              <textarea
                value={editableData.cover_letter_body}
                onChange={(e) => handleInputChange('cover_letter_body', e.target.value)}
                rows={12}
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent font-sans text-sm leading-relaxed"
                placeholder="Enter your cover letter content here..."
              />
            ) : (
              <div className="p-3 bg-gray-50 rounded border min-h-[300px]">
                <div className="whitespace-pre-wrap font-sans text-sm leading-relaxed">
                  {editableData.cover_letter_body}
                </div>
              </div>
            )}
          </div>

          {/* Action Buttons */}
          <div className="flex justify-end gap-3 pt-4">
            <Button variant="outline" onClick={handleCancel}>
              {isEditing ? 'Cancel Changes' : 'Back'}
            </Button>
            {isEditing && (
              <Button onClick={handleSave} className="bg-green-600 hover:bg-green-700">
                Save Changes
              </Button>
            )}
            {!isEditing && (
              <Button onClick={() => onSave(editableData)} className="bg-blue-600 hover:bg-blue-700">
                Generate PDF
              </Button>
            )}
          </div>
        </div>

        {/* Live Preview Panel */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-800">Live Preview</h3>
          
          <div className="bg-white border border-gray-300 rounded-lg p-6 shadow-sm min-h-[600px] font-serif text-sm leading-relaxed">
            {/* Header */}
            <div className="mb-8">
              <div className="text-lg font-bold text-gray-900 mb-2">
                {editableData.personal_details.full_name}
              </div>
              <div className="text-gray-600 text-sm space-y-1">
                <div>{editableData.personal_details.email}</div>
                <div>{editableData.personal_details.phone}</div>
                <div>{editableData.personal_details.location}</div>
                {editableData.personal_details.linkedin_url && (
                  <div>{editableData.personal_details.linkedin_url}</div>
                )}
              </div>
              
              <div className="text-right text-gray-600 text-sm mt-4">
                {editableData.generation_date}
              </div>
            </div>

            {/* Recipient */}
            <div className="mb-6 text-gray-700 text-sm">
              <div>Hiring Manager</div>
              <div>{editableData.company_name}</div>
              {editableData.include_company_address && editableData.company_address ? (
                <div className="whitespace-pre-wrap">{editableData.company_address}</div>
              ) : (
                <div>[Company Address]</div>
              )}
            </div>

            {/* Salutation */}
            <div className="mb-4 text-gray-900">
              {editableData.company_name && editableData.company_name !== "[Company Name]" 
                ? `Dear ${editableData.company_name} Hiring Team,`
                : "Dear Hiring Manager,"
              }
            </div>

            {/* Body */}
            <div className="mb-6 text-gray-900 text-justify">
              <div className="whitespace-pre-wrap">
                {editableData.cover_letter_body}
              </div>
            </div>

            {/* Closing */}
            <div className="space-y-4">
              <div>Sincerely,</div>
              <div className="font-semibold">{editableData.personal_details.full_name}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CoverLetterEditor;