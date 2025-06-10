// Gemini AI Service for Resume Building Assistance
// This service integrates with Google's Gemini AI for intelligent resume guidance

interface GeminiResponse {
  content: string;
  suggestions?: string[];
  improvements?: string[];
  score?: number;
}

interface CVAnalysis {
  strengths: string[];
  improvements: string[];
  score: number;
  atsCompatibility: number;
  suggestions: string[];
}

interface ResumeContext {
  currentStep: string;
  industry?: string;
  experience_level?: string;
  target_role?: string;
  cv_data?: any;
}

class GeminiService {
  private apiKey: string;
  private baseUrl: string = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent';

  constructor() {
    // In production, this should come from environment variables
    this.apiKey = process.env.NEXT_PUBLIC_GEMINI_API_KEY || '';
  }

  /**
   * Generate AI response for resume building assistance
   */
  async getResumeAdvice(
    userMessage: string, 
    context: ResumeContext
  ): Promise<GeminiResponse> {
    const prompt = this.buildPrompt(userMessage, context);
    
    try {
      const response = await fetch(`${this.baseUrl}?key=${this.apiKey}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          contents: [{
            parts: [{
              text: prompt
            }]
          }],
          generationConfig: {
            temperature: 0.7,
            topK: 40,
            topP: 0.95,
            maxOutputTokens: 1024,
          },
          safetySettings: [
            {
              category: "HARM_CATEGORY_HARASSMENT",
              threshold: "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
              category: "HARM_CATEGORY_HATE_SPEECH",
              threshold: "BLOCK_MEDIUM_AND_ABOVE"
            }
          ]
        })
      });

      if (!response.ok) {
        throw new Error(`Gemini API error: ${response.status}`);
      }

      const data = await response.json();
      const aiContent = data.candidates?.[0]?.content?.parts?.[0]?.text || '';
      
      return this.parseAIResponse(aiContent, context);
    } catch (error) {
      console.error('Gemini API Error:', error);
      return this.getFallbackResponse(userMessage, context);
    }
  }

  /**
   * Analyze complete resume and provide comprehensive feedback
   */
  async analyzeResume(cvData: any): Promise<CVAnalysis> {
    const analysisPrompt = `
As a professional resume expert, analyze this resume and provide detailed feedback:

RESUME DATA:
${JSON.stringify(cvData, null, 2)}

Please provide:
1. Strengths (3-5 points)
2. Areas for improvement (3-5 points)
3. Overall score (1-100)
4. ATS compatibility score (1-100)
5. Specific suggestions for enhancement

Format your response as JSON with these exact keys:
{
  "strengths": [],
  "improvements": [],
  "score": 0,
  "atsCompatibility": 0,
  "suggestions": []
}
`;

    try {
      const response = await this.getResumeAdvice(analysisPrompt, {
        currentStep: 'analysis',
        cv_data: cvData
      });

      // Try to parse as JSON, fallback to default structure
      try {
        return JSON.parse(response.content);
      } catch {
        return {
          strengths: [
            "Clear contact information",
            "Professional formatting",
            "Relevant work experience"
          ],
          improvements: [
            "Add more quantified achievements",
            "Strengthen professional summary",
            "Include relevant keywords"
          ],
          score: 75,
          atsCompatibility: 80,
          suggestions: [
            "Use action verbs to start bullet points",
            "Quantify achievements with numbers",
            "Tailor content to specific job roles"
          ]
        };
      }
    } catch (error) {
      console.error('Resume analysis error:', error);
      return this.getDefaultAnalysis();
    }
  }

  /**
   * Generate professional summary based on user input
   */
  async generateSummary(
    experience: string,
    skills: string[],
    targetRole: string,
    industry: string
  ): Promise<string> {
    const prompt = `
Write a compelling professional summary for a resume with these details:
- Experience: ${experience}
- Key Skills: ${skills.join(', ')}
- Target Role: ${targetRole}
- Industry: ${industry}

Requirements:
- 2-3 sentences maximum
- Professional tone
- Highlight key value proposition
- Include relevant keywords
- Focus on achievements and impact

Generate only the summary text, no additional formatting or explanation.
`;

    try {
      const response = await this.getResumeAdvice(prompt, {
        currentStep: 'summary',
        target_role: targetRole,
        industry: industry
      });

      return response.content || this.getDefaultSummary(targetRole);
    } catch (error) {
      console.error('Summary generation error:', error);
      return this.getDefaultSummary(targetRole);
    }
  }

  /**
   * Enhance job descriptions with AI
   */
  async enhanceJobDescription(
    jobTitle: string,
    company: string,
    description: string,
    achievements: string[]
  ): Promise<{ description: string; achievements: string[] }> {
    const prompt = `
Enhance this job experience for a professional resume:

Job Title: ${jobTitle}
Company: ${company}
Current Description: ${description}
Current Achievements: ${achievements.join('; ')}

Please:
1. Improve the job description (1-2 sentences, professional tone)
2. Enhance achievements with action verbs and quantifiable results
3. Make it ATS-friendly with relevant keywords

Return response in this format:
DESCRIPTION: [enhanced description]
ACHIEVEMENTS:
- [achievement 1]
- [achievement 2]
- [achievement 3]
`;

    try {
      const response = await this.getResumeAdvice(prompt, {
        currentStep: 'experience'
      });

      const content = response.content;
      const descriptionMatch = content.match(/DESCRIPTION:\s*(.+?)(?=ACHIEVEMENTS:|$)/s);
      const achievementsMatch = content.match(/ACHIEVEMENTS:\s*((?:-.+(?:\n|$))+)/s);

      const enhancedDescription = descriptionMatch?.[1]?.trim() || description;
      const enhancedAchievements = achievementsMatch?.[1]
        ?.split('\n')
        .map(line => line.replace(/^-\s*/, '').trim())
        .filter(Boolean) || achievements;

      return {
        description: enhancedDescription,
        achievements: enhancedAchievements
      };
    } catch (error) {
      console.error('Job description enhancement error:', error);
      return { description, achievements };
    }
  }

  /**
   * Suggest skills based on role and industry
   */
  async suggestSkills(
    currentRole: string,
    targetRole: string,
    industry: string,
    currentSkills: string[]
  ): Promise<{ technical: string[]; soft: string[]; trending: string[] }> {
    const prompt = `
Suggest relevant skills for this professional:
- Current Role: ${currentRole}
- Target Role: ${targetRole}
- Industry: ${industry}
- Current Skills: ${currentSkills.join(', ')}

Provide 3 categories:
1. Technical Skills (5-8 skills)
2. Soft Skills (4-6 skills)
3. Trending/In-demand Skills (3-5 skills)

Focus on skills that are:
- Relevant to the target role
- In-demand in the industry
- Not already listed in current skills
- ATS-friendly keywords

Format as:
TECHNICAL: skill1, skill2, skill3
SOFT: skill1, skill2, skill3
TRENDING: skill1, skill2, skill3
`;

    try {
      const response = await this.getResumeAdvice(prompt, {
        currentStep: 'skills',
        target_role: targetRole,
        industry: industry
      });

      const content = response.content;
      const technical = this.extractSkills(content, 'TECHNICAL');
      const soft = this.extractSkills(content, 'SOFT');
      const trending = this.extractSkills(content, 'TRENDING');

      return { technical, soft, trending };
    } catch (error) {
      console.error('Skills suggestion error:', error);
      return this.getDefaultSkills(targetRole);
    }
  }

  private buildPrompt(userMessage: string, context: ResumeContext): string {
    const basePrompt = `
You are an expert resume writer and career coach. You help professionals create outstanding resumes that get noticed by recruiters and pass ATS systems.

Current Context:
- Resume Section: ${context.currentStep}
- Industry: ${context.industry || 'Not specified'}
- Experience Level: ${context.experience_level || 'Not specified'}
- Target Role: ${context.target_role || 'Not specified'}

User Message: ${userMessage}

Guidelines:
- Provide specific, actionable advice
- Focus on ATS optimization
- Use professional language
- Include industry-specific keywords when relevant
- Keep responses concise but comprehensive
- Always end with 2-3 helpful suggestions as follow-up questions

Please provide a helpful response and suggest 2-3 follow-up questions the user might ask.
`;

    return basePrompt;
  }

  private parseAIResponse(content: string, context: ResumeContext): GeminiResponse {
    // Extract suggestions from the response
    const suggestionPatterns = [
      /(?:Questions?|Follow-up|Next|Consider|Try):\s*\n?((?:[-•]\s*.+(?:\n|$))+)/i,
      /(?:Suggestions?|Recommendations?):\s*\n?((?:[-•]\s*.+(?:\n|$))+)/i
    ];

    let suggestions: string[] = [];
    let cleanContent = content;

    for (const pattern of suggestionPatterns) {
      const match = content.match(pattern);
      if (match) {
        suggestions = match[1]
          .split('\n')
          .map(line => line.replace(/^[-•]\s*/, '').trim())
          .filter(Boolean)
          .slice(0, 3);
        
        cleanContent = content.replace(match[0], '').trim();
        break;
      }
    }

    // Default suggestions based on context
    if (suggestions.length === 0) {
      suggestions = this.getDefaultSuggestions(context.currentStep);
    }

    return {
      content: cleanContent,
      suggestions: suggestions
    };
  }

  private getFallbackResponse(userMessage: string, context: ResumeContext): GeminiResponse {
    const fallbackResponses = {
      header: "I'll help you create a professional header. Make sure to include your full name, phone number, professional email, city/state, and LinkedIn profile. Avoid including your full address for privacy.",
      summary: "Your professional summary should be 2-3 sentences highlighting your experience, key skills, and career goals. Focus on what makes you unique and valuable to employers.",
      experience: "For each role, focus on achievements rather than duties. Use action verbs like 'Led', 'Managed', 'Increased', and quantify your impact with numbers, percentages, or specific outcomes.",
      education: "List your education in reverse chronological order. Include degree, institution, graduation year, and relevant honors or achievements. You can omit graduation year if you're concerned about age discrimination.",
      skills: "Include both technical and soft skills relevant to your target role. Use keywords from job descriptions to improve ATS compatibility. Organize skills into categories for better readability.",
      default: "I'm here to help you create an outstanding resume! What specific area would you like assistance with?"
    };

    const response = fallbackResponses[context.currentStep as keyof typeof fallbackResponses] || fallbackResponses.default;
    
    return {
      content: response,
      suggestions: this.getDefaultSuggestions(context.currentStep)
    };
  }

  private getDefaultSuggestions(step: string): string[] {
    const suggestions = {
      header: [
        "What email format is most professional?",
        "Should I include my LinkedIn profile?",
        "How to format my phone number?"
      ],
      summary: [
        "Help me write a compelling summary",
        "What keywords should I include?",
        "How long should my summary be?"
      ],
      experience: [
        "How to quantify my achievements?",
        "What action verbs should I use?",
        "How to handle employment gaps?"
      ],
      education: [
        "Should I include my GPA?",
        "How to list incomplete degrees?",
        "Include relevant coursework?"
      ],
      skills: [
        "What skills are in-demand for my field?",
        "How many skills should I list?",
        "Technical vs soft skills balance?"
      ],
      default: [
        "Analyze my complete resume",
        "Suggest improvements",
        "Check ATS compatibility"
      ]
    };

    return suggestions[step as keyof typeof suggestions] || suggestions.default;
  }

  private extractSkills(content: string, category: string): string[] {
    const pattern = new RegExp(`${category}:\\s*(.+?)(?=\\n[A-Z]+:|$)`, 'i');
    const match = content.match(pattern);
    
    if (match) {
      return match[1]
        .split(',')
        .map(skill => skill.trim())
        .filter(Boolean)
        .slice(0, 8);
    }
    
    return [];
  }

  private getDefaultSkills(targetRole: string): { technical: string[]; soft: string[]; trending: string[] } {
    return {
      technical: ['Microsoft Office', 'Data Analysis', 'Project Management', 'CRM Software'],
      soft: ['Communication', 'Leadership', 'Problem Solving', 'Teamwork'],
      trending: ['Digital Marketing', 'Remote Collaboration', 'Agile Methodology']
    };
  }

  private getDefaultSummary(targetRole: string): string {
    return `Experienced professional with a proven track record of success in ${targetRole.toLowerCase()}. Strong analytical and communication skills with the ability to drive results in fast-paced environments. Seeking to leverage expertise to contribute to organizational growth and success.`;
  }

  private getDefaultAnalysis(): CVAnalysis {
    return {
      strengths: [
        "Professional formatting and layout",
        "Clear contact information",
        "Relevant work experience included"
      ],
      improvements: [
        "Add more quantified achievements",
        "Strengthen professional summary",
        "Include industry-specific keywords",
        "Optimize for ATS compatibility"
      ],
      score: 72,
      atsCompatibility: 75,
      suggestions: [
        "Use action verbs to start bullet points",
        "Quantify achievements with specific numbers",
        "Tailor content to match job descriptions",
        "Add relevant technical skills",
        "Include professional certifications"
      ]
    };
  }
}

// Export singleton instance
export const geminiService = new GeminiService();

// Export types for use in components
export type { GeminiResponse, CVAnalysis, ResumeContext };