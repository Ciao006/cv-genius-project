import React from 'react';
import { ENVIRONMENT, URLS } from '@/utils/constants';

const EnvironmentIndicator: React.FC = () => {
  // Only show in development mode
  if (!ENVIRONMENT.isDevelopment) {
    return null;
  }

  const apiUrl = ENVIRONMENT.isDevelopment 
    ? URLS.DEVELOPMENT_API
    : 'Production Backend';

  return (
    <div className="fixed top-4 right-4 z-50 bg-green-500 text-white px-3 py-1 rounded-lg text-sm font-medium shadow-lg">
      🛠️ DEV MODE - API: {apiUrl}
    </div>
  );
};

export default EnvironmentIndicator; 