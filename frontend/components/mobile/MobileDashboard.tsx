import React, { useState, useEffect } from 'react';
import {
  PlusIcon,
  EyeIcon,
  PencilIcon,
  DocumentArrowDownIcon,
  ShareIcon,
  TrashIcon,
  ChartBarIcon,
  StarIcon,
  ClockIcon,
  UserIcon,
  BriefcaseIcon,
  AcademicCapIcon
} from '@heroicons/react/24/outline';

interface CVItem {
  id: string;
  name: string;
  template: string;
  lastModified: Date;
  isStarred: boolean;
  analytics: {
    views: number;
    downloads: number;
    applications: number;
    atsScore: number;
  };
  thumbnail?: string;
}

interface MobileDashboardProps {
  cvs: CVItem[];
  onCreateNew: () => void;
  onEditCV: (id: string) => void;
  onPreviewCV: (id: string) => void;
  onDeleteCV: (id: string) => void;
  onStarCV: (id: string) => void;
  onExportCV: (id: string, format: string) => void;
  onShareCV: (id: string) => void;
  onViewAnalytics: (id: string) => void;
}

const MobileDashboard: React.FC<MobileDashboardProps> = ({
  cvs,
  onCreateNew,
  onEditCV,
  onPreviewCV,
  onDeleteCV,
  onStarCV,
  onExportCV,
  onShareCV,
  onViewAnalytics
}) => {
  const [selectedCV, setSelectedCV] = useState<string | null>(null);
  const [showActions, setShowActions] = useState(false);
  const [sortBy, setSortBy] = useState<'modified' | 'name' | 'views'>('modified');
  const [filterStarred, setFilterStarred] = useState(false);

  // Sort and filter CVs
  const sortedCVs = [...cvs]
    .filter(cv => !filterStarred || cv.isStarred)
    .sort((a, b) => {
      switch (sortBy) {
        case 'name':
          return a.name.localeCompare(b.name);
        case 'views':
          return b.analytics.views - a.analytics.views;
        case 'modified':
        default:
          return b.lastModified.getTime() - a.lastModified.getTime();
      }
    });

  const formatDate = (date: Date) => {
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays} days ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
    return date.toLocaleDateString();
  };

  const getATSScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-100';
    if (score >= 60) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const handleCVSelect = (cvId: string) => {
    if (selectedCV === cvId) {
      setSelectedCV(null);
      setShowActions(false);
    } else {
      setSelectedCV(cvId);
      setShowActions(true);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b sticky top-0 z-10">
        <div className="px-4 py-4">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-2xl font-bold text-gray-800">My CVs</h1>
            <button
              onClick={onCreateNew}
              className="flex items-center px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              <PlusIcon className="w-5 h-5 mr-2" />
              New CV
            </button>
          </div>

          {/* Filters and Sort */}
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <button
                onClick={() => setFilterStarred(!filterStarred)}
                className={`flex items-center px-3 py-1 rounded-full text-sm ${
                  filterStarred
                    ? 'bg-yellow-100 text-yellow-800'
                    : 'bg-gray-100 text-gray-600'
                }`}
              >
                <StarIcon className="w-4 h-4 mr-1" />
                Starred
              </button>

              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as any)}
                className="px-3 py-1 border border-gray-300 rounded-lg text-sm"
              >
                <option value="modified">Recent</option>
                <option value="name">Name</option>
                <option value="views">Most Viewed</option>
              </select>
            </div>

            <div className="text-sm text-gray-600">
              {sortedCVs.length} CV{sortedCVs.length !== 1 ? 's' : ''}
            </div>
          </div>
        </div>
      </div>

      {/* CV List */}
      <div className="px-4 py-4 space-y-3">
        {sortedCVs.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-gray-400 mb-4">
              <BriefcaseIcon className="w-16 h-16 mx-auto" />
            </div>
            <h3 className="text-lg font-medium text-gray-600 mb-2">
              {filterStarred ? 'No starred CVs' : 'No CVs yet'}
            </h3>
            <p className="text-gray-500 mb-6">
              {filterStarred 
                ? 'Star your favorite CVs to see them here'
                : 'Create your first CV to get started'
              }
            </p>
            {!filterStarred && (
              <button
                onClick={onCreateNew}
                className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
              >
                Create Your First CV
              </button>
            )}
          </div>
        ) : (
          sortedCVs.map((cv) => (
            <div
              key={cv.id}
              className={`bg-white rounded-lg border p-4 ${
                selectedCV === cv.id 
                  ? 'border-blue-500 bg-blue-50' 
                  : 'border-gray-200'
              }`}
              onClick={() => handleCVSelect(cv.id)}
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-1">
                    <h3 className="font-semibold text-gray-800 text-lg">
                      {cv.name}
                    </h3>
                    {cv.isStarred && (
                      <StarIcon className="w-4 h-4 text-yellow-500 fill-current" />
                    )}
                  </div>
                  
                  <div className="flex items-center space-x-4 text-sm text-gray-600 mb-2">
                    <span className="flex items-center">
                      <ClockIcon className="w-4 h-4 mr-1" />
                      {formatDate(cv.lastModified)}
                    </span>
                    <span className="capitalize">{cv.template} template</span>
                  </div>

                  {/* Analytics Summary */}
                  <div className="flex items-center space-x-4 text-xs">
                    <span className="flex items-center text-gray-600">
                      <EyeIcon className="w-3 h-3 mr-1" />
                      {cv.analytics.views} views
                    </span>
                    <span className="flex items-center text-gray-600">
                      <DocumentArrowDownIcon className="w-3 h-3 mr-1" />
                      {cv.analytics.downloads} downloads
                    </span>
                    <span className="flex items-center text-gray-600">
                      <BriefcaseIcon className="w-3 h-3 mr-1" />
                      {cv.analytics.applications} applications
                    </span>
                  </div>
                </div>

                {/* ATS Score */}
                <div className="ml-4">
                  <div className={`px-2 py-1 rounded-full text-xs font-medium ${getATSScoreColor(cv.analytics.atsScore)}`}>
                    ATS: {cv.analytics.atsScore}%
                  </div>
                </div>
              </div>

              {/* Quick Actions */}
              <div className="flex items-center justify-between pt-3 border-t border-gray-100">
                <div className="flex items-center space-x-3">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onPreviewCV(cv.id);
                    }}
                    className="flex items-center text-gray-600 hover:text-blue-600"
                  >
                    <EyeIcon className="w-4 h-4 mr-1" />
                    <span className="text-sm">View</span>
                  </button>

                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onEditCV(cv.id);
                    }}
                    className="flex items-center text-gray-600 hover:text-blue-600"
                  >
                    <PencilIcon className="w-4 h-4 mr-1" />
                    <span className="text-sm">Edit</span>
                  </button>

                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onViewAnalytics(cv.id);
                    }}
                    className="flex items-center text-gray-600 hover:text-green-600"
                  >
                    <ChartBarIcon className="w-4 h-4 mr-1" />
                    <span className="text-sm">Stats</span>
                  </button>
                </div>

                <div className="flex items-center space-x-2">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onStarCV(cv.id);
                    }}
                    className={`p-1 ${
                      cv.isStarred 
                        ? 'text-yellow-500' 
                        : 'text-gray-400 hover:text-yellow-500'
                    }`}
                  >
                    <StarIcon className={`w-4 h-4 ${cv.isStarred ? 'fill-current' : ''}`} />
                  </button>

                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onShareCV(cv.id);
                    }}
                    className="p-1 text-gray-400 hover:text-blue-500"
                  >
                    <ShareIcon className="w-4 h-4" />
                  </button>

                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onExportCV(cv.id, 'pdf');
                    }}
                    className="p-1 text-gray-400 hover:text-green-500"
                  >
                    <DocumentArrowDownIcon className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Action Sheet */}
      {showActions && selectedCV && (
        <div className="fixed inset-x-0 bottom-0 bg-white border-t shadow-lg z-20">
          <div className="px-4 py-6">
            <div className="grid grid-cols-2 gap-4">
              <button
                onClick={() => {
                  onEditCV(selectedCV);
                  setShowActions(false);
                  setSelectedCV(null);
                }}
                className="flex flex-col items-center justify-center py-4 bg-blue-500 text-white rounded-lg"
              >
                <PencilIcon className="w-6 h-6 mb-2" />
                <span className="text-sm font-medium">Edit</span>
              </button>

              <button
                onClick={() => {
                  onPreviewCV(selectedCV);
                  setShowActions(false);
                  setSelectedCV(null);
                }}
                className="flex flex-col items-center justify-center py-4 bg-gray-500 text-white rounded-lg"
              >
                <EyeIcon className="w-6 h-6 mb-2" />
                <span className="text-sm font-medium">Preview</span>
              </button>

              <button
                onClick={() => {
                  onExportCV(selectedCV, 'pdf');
                  setShowActions(false);
                  setSelectedCV(null);
                }}
                className="flex flex-col items-center justify-center py-4 bg-green-500 text-white rounded-lg"
              >
                <DocumentArrowDownIcon className="w-6 h-6 mb-2" />
                <span className="text-sm font-medium">Download</span>
              </button>

              <button
                onClick={() => {
                  onViewAnalytics(selectedCV);
                  setShowActions(false);
                  setSelectedCV(null);
                }}
                className="flex flex-col items-center justify-center py-4 bg-purple-500 text-white rounded-lg"
              >
                <ChartBarIcon className="w-6 h-6 mb-2" />
                <span className="text-sm font-medium">Analytics</span>
              </button>

              <button
                onClick={() => {
                  onShareCV(selectedCV);
                  setShowActions(false);
                  setSelectedCV(null);
                }}
                className="flex flex-col items-center justify-center py-4 bg-indigo-500 text-white rounded-lg"
              >
                <ShareIcon className="w-6 h-6 mb-2" />
                <span className="text-sm font-medium">Share</span>
              </button>

              <button
                onClick={() => {
                  onStarCV(selectedCV);
                  setShowActions(false);
                  setSelectedCV(null);
                }}
                className="flex flex-col items-center justify-center py-4 bg-yellow-500 text-white rounded-lg"
              >
                <StarIcon className="w-6 h-6 mb-2" />
                <span className="text-sm font-medium">
                  {cvs.find(cv => cv.id === selectedCV)?.isStarred ? 'Unstar' : 'Star'}
                </span>
              </button>
            </div>

            {/* Close Action Sheet */}
            <div className="mt-4">
              <button
                onClick={() => {
                  setShowActions(false);
                  setSelectedCV(null);
                }}
                className="w-full py-3 text-gray-600 border border-gray-300 rounded-lg"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Floating Action Button (Alternative) */}
      {!showActions && (
        <button
          onClick={onCreateNew}
          className="fixed bottom-6 right-6 w-14 h-14 bg-blue-500 text-white rounded-full shadow-lg hover:bg-blue-600 flex items-center justify-center z-10"
        >
          <PlusIcon className="w-6 h-6" />
        </button>
      )}

      {/* Quick Stats Bar */}
      {cvs.length > 0 && (
        <div className="fixed bottom-0 left-0 right-0 bg-white border-t px-4 py-2 text-xs text-gray-600">
          <div className="flex justify-center space-x-6">
            <span>{cvs.length} CVs</span>
            <span>{cvs.filter(cv => cv.isStarred).length} starred</span>
            <span>{cvs.reduce((sum, cv) => sum + cv.analytics.views, 0)} total views</span>
            <span>{cvs.reduce((sum, cv) => sum + cv.analytics.applications, 0)} applications</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default MobileDashboard;