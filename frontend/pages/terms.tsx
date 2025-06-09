import React from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { ArrowLeft, Scale, AlertTriangle, CheckCircle, XCircle } from 'lucide-react';

const TermsOfServicePage: React.FC = () => {
  return (
    <>
      <Head>
        <title>Terms of Service - CVGenius</title>
        <meta name="description" content="CVGenius Terms of Service - Your rights and responsibilities when using our AI-powered CV generation service" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="container mx-auto px-4 py-8">
          {/* Header */}
          <div className="mb-8">
            <Link 
              href="/" 
              className="inline-flex items-center text-blue-600 hover:text-blue-800 transition-colors mb-4"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Home
            </Link>
            <h1 className="text-4xl font-bold text-gray-900 mb-4">Terms of Service</h1>
            <p className="text-gray-600 text-lg">
              Last updated: {new Date().toLocaleDateString('en-IE', { 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
              })}
            </p>
          </div>

          <div className="max-w-4xl mx-auto">
            {/* Key Terms Highlights */}
            <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
                <Scale className="w-6 h-6 mr-3 text-blue-600" />
                Key Terms Summary
              </h2>
              
              <div className="grid md:grid-cols-2 gap-6">
                <div className="bg-green-50 rounded-lg p-4">
                  <div className="flex items-center mb-2">
                    <CheckCircle className="w-5 h-5 mr-2 text-green-600" />
                    <h3 className="font-semibold text-green-800">What You Get</h3>
                  </div>
                  <ul className="text-green-700 text-sm space-y-1">
                    <li>• AI-powered CV and cover letter generation</li>
                    <li>• Professional formatting and optimization</li>
                    <li>• Instant PDF downloads</li>
                    <li>• Free service with usage limits</li>
                  </ul>
                </div>
                
                <div className="bg-blue-50 rounded-lg p-4">
                  <div className="flex items-center mb-2">
                    <AlertTriangle className="w-5 h-5 mr-2 text-blue-600" />
                    <h3 className="font-semibold text-blue-800">Your Responsibilities</h3>
                  </div>
                  <ul className="text-blue-700 text-sm space-y-1">
                    <li>• Provide accurate information</li>
                    <li>• Use service for personal/professional purposes</li>
                    <li>• Respect usage limits and fair use</li>
                    <li>• No abuse or automated access</li>
                  </ul>
                </div>
                
                <div className="bg-orange-50 rounded-lg p-4">
                  <div className="flex items-center mb-2">
                    <XCircle className="w-5 h-5 mr-2 text-orange-600" />
                    <h3 className="font-semibold text-orange-800">What We Do Not Do</h3>
                  </div>
                  <ul className="text-orange-700 text-sm space-y-1">
                    <li>• Store your personal data</li>
                    <li>• Guarantee job placement success</li>
                    <li>• Provide employment advice</li>
                    <li>• Share your information with employers</li>
                  </ul>
                </div>
                
                <div className="bg-purple-50 rounded-lg p-4">
                  <div className="flex items-center mb-2">
                    <Scale className="w-5 h-5 mr-2 text-purple-600" />
                    <h3 className="font-semibold text-purple-800">Legal Basis</h3>
                  </div>
                  <ul className="text-purple-700 text-sm space-y-1">
                    <li>• Governed by Irish law</li>
                    <li>• GDPR compliant service</li>
                    <li>• No warranty or liability</li>
                    <li>• Service provided as is</li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Main Content */}
            <div className="bg-white rounded-xl shadow-lg p-8 space-y-8">
              {/* Acceptance */}
              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">1. Acceptance of Terms</h2>
                <p className="text-gray-700 leading-relaxed mb-4">
                  By accessing and using CVGenius (the Service), you accept and agree to be bound by the terms 
                  and provision of this agreement. If you do not agree to these Terms of Service, you should not use this service.
                </p>
                <p className="text-gray-700 leading-relaxed">
                  These terms apply to all visitors, users, and others who access or use the service, regardless 
                  of whether they create an account or use the service as a guest.
                </p>
              </section>

              {/* Service Description */}
              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">2. Service Description</h2>
                
                <h3 className="text-lg font-semibold text-gray-800 mb-3">What CVGenius Provides:</h3>
                <ul className="list-disc list-inside text-gray-700 mb-4 space-y-2">
                  <li><strong>AI-Powered CV Generation:</strong> Create professional CVs from your personal and professional information</li>
                  <li><strong>Cover Letter Creation:</strong> Generate tailored cover letters for specific job applications</li>
                  <li><strong>CV Optimization:</strong> Enhance existing CVs by uploading your current CV file</li>
                  <li><strong>PDF Generation:</strong> Download professional, ATS-friendly PDF documents</li>
                  <li><strong>Job Targeting:</strong> Customize content based on specific job descriptions</li>
                </ul>

                <div className="bg-blue-50 rounded-lg p-4">
                  <h4 className="font-semibold text-blue-800 mb-2">How It Works:</h4>
                  <ol className="list-decimal list-inside text-blue-700 space-y-1 text-sm">
                    <li>You provide your information through our web forms or file uploads</li>
                    <li>Our AI processes and enhances your content</li>
                    <li>Professional documents are generated and returned to you</li>
                    <li>Your data is immediately deleted from our systems</li>
                  </ol>
                </div>
              </section>

              {/* User Responsibilities */}
              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">3. User Responsibilities and Acceptable Use</h2>
                
                <h3 className="text-lg font-semibold text-gray-800 mb-3">You agree to:</h3>
                <ul className="list-disc list-inside text-gray-700 mb-4 space-y-1">
                  <li>Provide accurate and truthful information about your qualifications and experience</li>
                  <li>Use the service for personal and professional purposes only</li>
                  <li>Respect the usage limits and rate limiting in place</li>
                  <li>Not attempt to reverse engineer, hack, or abuse the service</li>
                  <li>Not use automated tools or bots to access the service</li>
                  <li>Not upload malicious files or content</li>
                  <li>Comply with all applicable laws and regulations</li>
                </ul>

                <h3 className="text-lg font-semibold text-gray-800 mb-3">Prohibited Uses:</h3>
                <div className="bg-red-50 rounded-lg p-4">
                  <ul className="list-disc list-inside text-red-700 space-y-1 text-sm">
                    <li>Creating false or misleading CVs with fabricated information</li>
                    <li>Using the service for commercial resale or bulk generation</li>
                    <li>Attempting to overload or disrupt our servers</li>
                    <li>Uploading copyrighted content without permission</li>
                    <li>Using the service for illegal activities</li>
                    <li>Circumventing rate limits or usage restrictions</li>
                  </ul>
                </div>
              </section>

              {/* Usage Limits */}
              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">4. Usage Limits and Fair Use</h2>
                
                <div className="bg-yellow-50 rounded-lg p-4 mb-4">
                  <h3 className="text-lg font-semibold text-yellow-800 mb-2">Current Limits:</h3>
                  <ul className="text-yellow-700 space-y-1 text-sm">
                    <li><strong>Rate Limit:</strong> 15 requests per hour per IP address</li>
                    <li><strong>File Size:</strong> Maximum 5MB for uploaded CV files</li>
                    <li><strong>Supported Formats:</strong> PDF and DOCX files only</li>
                    <li><strong>Fair Use:</strong> Personal and professional use only</li>
                  </ul>
                </div>
                
                <p className="text-gray-700">
                  These limits are in place to ensure fair access for all users and to prevent abuse. If you need 
                  higher limits for legitimate business use, please contact us to discuss enterprise options.
                </p>
              </section>

              {/* Intellectual Property */}
              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">5. Intellectual Property Rights</h2>
                
                <h3 className="text-lg font-semibold text-gray-800 mb-3">Your Content:</h3>
                <p className="text-gray-700 mb-4">
                  You retain all rights to the information you provide to CVGenius. The content of your CV, including 
                  your personal information, work experience, and qualifications, remains your intellectual property.
                </p>

                <h3 className="text-lg font-semibold text-gray-800 mb-3">Generated Content:</h3>
                <p className="text-gray-700 mb-4">
                  The enhanced CV and cover letter content generated by our AI becomes your property upon creation. 
                  You are free to use, modify, and distribute these documents as you see fit.
                </p>

                <h3 className="text-lg font-semibold text-gray-800 mb-3">Service Technology:</h3>
                <p className="text-gray-700">
                  The CVGenius service, including our AI models, templates, algorithms, and software, remains our 
                  intellectual property. You may not copy, reverse engineer, or create derivative works based on our service technology.
                </p>
              </section>

              {/* Privacy and Data */}
              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">6. Privacy and Data Handling</h2>
                
                <div className="bg-green-50 rounded-lg p-4">
                  <h3 className="text-lg font-semibold text-green-800 mb-2">Data Protection Promise:</h3>
                  <ul className="text-green-700 space-y-2 text-sm">
                    <li><strong>No Storage:</strong> We do not store your personal information or CV content</li>
                    <li><strong>Immediate Deletion:</strong> All data is deleted after processing</li>
                    <li><strong>GDPR Compliant:</strong> Full compliance with EU data protection laws</li>
                    <li><strong>Secure Processing:</strong> All data transmission is encrypted</li>
                  </ul>
                </div>
                
                <p className="text-gray-700 mt-4">
                  For detailed information about how we handle your data, please refer to our 
                  <Link href="/privacy" className="text-blue-600 hover:text-blue-800 underline ml-1">
                    Privacy Policy
                  </Link>.
                </p>
              </section>

              {/* Disclaimers */}
              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">7. Disclaimers and Limitations</h2>
                
                <div className="bg-gray-50 rounded-lg p-4 mb-4">
                  <h3 className="text-lg font-semibold text-gray-800 mb-2">Important Disclaimers:</h3>
                  <ul className="text-gray-700 space-y-2 text-sm">
                    <li><strong>No Guarantee of Success:</strong> We cannot guarantee that using our service will result in job interviews or employment</li>
                    <li><strong>AI-Generated Content:</strong> Our AI enhances your content but you should review and verify all generated information</li>
                    <li><strong>Not Career Advice:</strong> We provide document generation, not professional career counseling</li>
                    <li><strong>Service Availability:</strong> We strive for 99.9% uptime but cannot guarantee uninterrupted service</li>
                  </ul>
                </div>

                <h3 className="text-lg font-semibold text-gray-800 mb-3">Service As Is:</h3>
                <p className="text-gray-700">
                  CVGenius is provided as is without any warranties, express or implied. We make no representations 
                  about the suitability, reliability, availability, timeliness, or accuracy of the service for any purpose.
                </p>
              </section>

              {/* Limitation of Liability */}
              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">8. Limitation of Liability</h2>
                
                <p className="text-gray-700 mb-4">
                  To the maximum extent permitted by law, CVGenius and its operators shall not be liable for any indirect, 
                  incidental, special, consequential, or punitive damages, including without limitation, loss of profits, 
                  data, use, goodwill, or other intangible losses.
                </p>
                
                <div className="bg-orange-50 rounded-lg p-4">
                  <h3 className="text-lg font-semibold text-orange-800 mb-2">Specific Limitations:</h3>
                  <ul className="text-orange-700 space-y-1 text-sm">
                    <li>• No liability for job application outcomes</li>
                    <li>• No responsibility for employer decisions</li>
                    <li>• No liability for technical issues or service interruptions</li>
                    <li>• Maximum liability limited to the amount paid for services (€0 for free users)</li>
                  </ul>
                </div>
              </section>

              {/* Termination */}
              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">9. Termination and Suspension</h2>
                
                <h3 className="text-lg font-semibold text-gray-800 mb-3">Your Right to Stop Using:</h3>
                <p className="text-gray-700 mb-4">
                  You may stop using our service at any time without notice. Since we do not store your data, 
                  there are no accounts to delete or data to remove.
                </p>

                <h3 className="text-lg font-semibold text-gray-800 mb-3">Our Right to Suspend Access:</h3>
                <p className="text-gray-700 mb-4">
                  We reserve the right to suspend or terminate access to our service for users who:
                </p>
                <ul className="list-disc list-inside text-gray-700 space-y-1">
                  <li>Violate these Terms of Service</li>
                  <li>Engage in abuse or misuse of the service</li>
                  <li>Attempt to circumvent usage limits</li>
                  <li>Use automated tools to access the service</li>
                  <li>Engage in illegal activities</li>
                </ul>
              </section>

              {/* Changes to Terms */}
              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">10. Changes to Terms</h2>
                
                <p className="text-gray-700 mb-4">
                  We reserve the right to modify these Terms of Service at any time. Changes will be effective when 
                  posted on this page with an updated Last updated date.
                </p>
                
                <div className="bg-blue-50 rounded-lg p-4">
                  <p className="text-blue-700 text-sm">
                    <strong>Notification:</strong> For significant changes, we will provide notice through our service or website. 
                    Continued use of the service after changes constitutes acceptance of the new terms.
                  </p>
                </div>
              </section>

              {/* Governing Law */}
              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">11. Governing Law and Jurisdiction</h2>
                
                <p className="text-gray-700 mb-4">
                  These Terms of Service are governed by and construed in accordance with the laws of Ireland. 
                  Any disputes arising from these terms or the use of our service will be subject to the exclusive 
                  jurisdiction of the Irish courts.
                </p>
                
                <h3 className="text-lg font-semibold text-gray-800 mb-3">Dispute Resolution:</h3>
                <ol className="list-decimal list-inside text-gray-700 space-y-1">
                  <li>Contact us first to try to resolve the issue informally</li>
                  <li>If informal resolution fails, disputes may be brought before Irish courts</li>
                  <li>EU users may also use the European Commission Online Dispute Resolution platform</li>
                </ol>
              </section>

              {/* Contact Information */}
              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">12. Contact Information</h2>
                
                <div className="bg-gray-50 rounded-lg p-4">
                  <p className="text-gray-700 mb-3">
                    If you have questions about these Terms of Service or need to report a violation, please contact us.
                  </p>
                  
                  <div className="space-y-2 text-gray-600">
                    <p><strong>Service:</strong> CVGenius</p>
                    <p><strong>Jurisdiction:</strong> Ireland</p>
                    <p><strong>Response Time:</strong> Within 72 hours for terms-related inquiries</p>
                    <p><strong>Legal Compliance:</strong> Irish law and EU regulations</p>
                  </div>
                </div>
              </section>

              {/* Severability */}
              <section className="border-t pt-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">13. Severability</h2>
                
                <p className="text-gray-700">
                  If any provision of these Terms of Service is found to be unenforceable or invalid, that provision 
                  will be limited or eliminated to the minimum extent necessary so that these terms will otherwise 
                  remain in full force and effect.
                </p>
              </section>
            </div>

            {/* Footer */}
            <div className="text-center mt-8 p-4 bg-white rounded-lg shadow">
              <p className="text-gray-600 text-sm mb-2">
                These Terms of Service are effective as of {new Date().toLocaleDateString('en-IE')} and apply to all users of CVGenius.
              </p>
              <p className="text-gray-500 text-xs">
                By using our service, you acknowledge that you have read, understood, and agree to be bound by these terms.
              </p>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default TermsOfServicePage;