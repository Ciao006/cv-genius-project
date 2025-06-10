// CV Data Persistence Service
// This service handles saving and retrieving CV data from the backend

interface CVDataResponse {
  success: boolean;
  data?: any;
  message?: string;
  id?: string;
}

interface SaveCVRequest {
  cv_data: any;
  template_id?: string;
  user_id?: string;
  title?: string;
}

class CVDataService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  }

  /**
   * Save CV data to backend
   */
  async saveCVData(data: SaveCVRequest): Promise<CVDataResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/api/v1/cv/save`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      return {
        success: true,
        data: result,
        id: result.id
      };
    } catch (error) {
      console.error('Save CV Error:', error);
      return {
        success: false,
        message: error instanceof Error ? error.message : 'Failed to save CV data'
      };
    }
  }

  /**
   * Load CV data from backend
   */
  async loadCVData(cvId: string): Promise<CVDataResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/api/v1/cv/${cvId}`);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      return {
        success: true,
        data: result
      };
    } catch (error) {
      console.error('Load CV Error:', error);
      return {
        success: false,
        message: error instanceof Error ? error.message : 'Failed to load CV data'
      };
    }
  }

  /**
   * Generate PDF from CV data
   */
  async generatePDF(cvData: any, templateId: string = 'professional'): Promise<CVDataResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/api/v1/cv/generate-pdf`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          cv_data: cvData,
          template_id: templateId
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      return {
        success: true,
        data: result
      };
    } catch (error) {
      console.error('Generate PDF Error:', error);
      return {
        success: false,
        message: error instanceof Error ? error.message : 'Failed to generate PDF'
      };
    }
  }

  /**
   * Get user's CV list
   */
  async getUserCVs(userId: string): Promise<CVDataResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/api/v1/cv/user/${userId}`);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      return {
        success: true,
        data: result
      };
    } catch (error) {
      console.error('Get User CVs Error:', error);
      return {
        success: false,
        message: error instanceof Error ? error.message : 'Failed to load user CVs'
      };
    }
  }

  /**
   * Delete CV
   */
  async deleteCVData(cvId: string): Promise<CVDataResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/api/v1/cv/${cvId}`, {
        method: 'DELETE'
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return {
        success: true,
        message: 'CV deleted successfully'
      };
    } catch (error) {
      console.error('Delete CV Error:', error);
      return {
        success: false,
        message: error instanceof Error ? error.message : 'Failed to delete CV'
      };
    }
  }

  /**
   * Auto-save CV data (debounced)
   */
  private autoSaveTimer: NodeJS.Timeout | null = null;

  autoSave(cvData: any, cvId?: string, delay: number = 2000): Promise<CVDataResponse> {
    return new Promise((resolve) => {
      // Clear existing timer
      if (this.autoSaveTimer) {
        clearTimeout(this.autoSaveTimer);
      }

      // Set new timer
      this.autoSaveTimer = setTimeout(async () => {
        const result = await this.saveCVData({
          cv_data: cvData,
          title: `CV - ${cvData.personal?.firstName || 'Untitled'}`
        });
        resolve(result);
      }, delay);
    });
  }

  /**
   * Validate CV data completeness
   */
  validateCVData(cvData: any): { isValid: boolean; missingFields: string[]; score: number } {
    const missingFields: string[] = [];
    let score = 0;
    const maxScore = 100;

    // Required fields check
    if (!cvData.personal?.firstName) missingFields.push('First Name');
    else score += 10;

    if (!cvData.personal?.lastName) missingFields.push('Last Name');
    else score += 10;

    if (!cvData.personal?.email) missingFields.push('Email');
    else score += 15;

    if (!cvData.personal?.phone) missingFields.push('Phone');
    else score += 10;

    if (!cvData.summary || cvData.summary.length < 50) missingFields.push('Professional Summary');
    else score += 20;

    if (!cvData.experience || cvData.experience.length === 0) missingFields.push('Work Experience');
    else score += 25;

    if (!cvData.skills?.technical?.length && !cvData.skills?.soft?.length) missingFields.push('Skills');
    else score += 10;

    return {
      isValid: missingFields.length === 0,
      missingFields,
      score: Math.min(score, maxScore)
    };
  }
}

// Export singleton instance
export const cvDataService = new CVDataService();

// Export types for use in components
export type { CVDataResponse, SaveCVRequest };