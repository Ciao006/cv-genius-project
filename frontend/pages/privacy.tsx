import React from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { ArrowLeft, Shield, Database, Eye, Lock } from 'lucide-react';

const PrivacyPolicyPage: React.FC = () => {
  return (
    <>
      <Head>
        <title>Privacy Policy - CVGenius</title>
        <meta name="description" content="CVGenius Privacy Policy - Learn how we protect your data and privacy" />
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
            <h1 className="text-4xl font-bold text-gray-900 mb-4">Privacy Policy</h1>
            <p className="text-gray-600 text-lg">
              Last updated: {new Date().toLocaleDateString('en-IE', { 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
              })}
            </p>
          </div>

          <div className="max-w-4xl mx-auto">
            {/* Privacy Highlights */}
            <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
                <Shield className="w-6 h-6 mr-3 text-green-600" />
                Your Privacy at a Glance
              </h2>
              
              <div className="grid md:grid-cols-2 gap-6">
                <div className="bg-green-50 rounded-lg p-4">
                  <div className="flex items-center mb-2">
                    <Database className="w-5 h-5 mr-2 text-green-600" />
                    <h3 className="font-semibold text-green-800">No Data Storage</h3>
                  </div>
                  <p className="text-green-700 text-sm">
                    We do not store your CV content, personal information, or job descriptions on our servers.
                  </p>
                </div>
                
                <div className="bg-blue-50 rounded-lg p-4">
                  <div className="flex items-center mb-2">
                    <Eye className="w-5 h-5 mr-2 text-blue-600" />
                    <h3 className="font-semibold text-blue-800">No Tracking</h3>
                  </div>
                  <p className="text-blue-700 text-sm">
                    We do not use cookies for tracking or collect personal browsing data.
                  </p>
                </div>
                
                <div className="bg-purple-50 rounded-lg p-4">
                  <div className="flex items-center mb-2">
                    <Lock className="w-5 h-5 mr-2 text-purple-600" />
                    <h3 className="font-semibold text-purple-800">Secure Processing</h3>
                  </div>
                  <p className="text-purple-700 text-sm">
                    Your data is processed securely and deleted immediately after PDF generation.
                  </p>
                </div>
                
                <div className="bg-orange-50 rounded-lg p-4">
                  <div className="flex items-center mb-2">
                    <Shield className="w-5 h-5 mr-2 text-orange-600" />
                    <h3 className="font-semibold text-orange-800">GDPR Compliant</h3>
                  </div>
                  <p className="text-orange-700 text-sm">
                    Fully compliant with EU data protection regulations and Irish law.
                  </p>
                </div>
              </div>
            </div>

            {/* Main Content */}
            <div className="bg-white rounded-xl shadow-lg p-8 space-y-8">
              {/* Introduction */}
              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Introduction</h2>
                <p className="text-gray-700 leading-relaxed">
                  CVGenius is committed to protecting your privacy. This Privacy Policy explains how we handle 
                  information when you use our AI-powered CV and cover letter generation service. Our service is 
                  designed with privacy by design principles - we do not store your personal data.
                </p>
              </section>

              {/* What We Process */}
              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Information We Process</h2>
                
                <h3 className="text-lg font-semibold text-gray-800 mb-3">Personal Information for CV Generation</h3>
                <p className="text-gray-700 mb-3">When you create a CV, you provide:</p>
                <ul className="list-disc list-inside text-gray-700 mb-4 space-y-1">
                  <li>Contact details (name, email, phone, location)</li>
                  <li>Work experience and employment history</li>
                  <li>Education background</li>
                  <li>Skills and qualifications</li>
                  <li>Job descriptions for targeting (optional)</li>
                </ul>

                <h3 className="text-lg font-semibold text-gray-800 mb-3">File Uploads</h3>
                <p className="text-gray-700 mb-4">
                  When using our CV update feature, you may upload existing CV files (PDF, DOCX). 
                  These files are processed to extract text content for enhancement.
                </p>
              </section>

              {/* How We Process */}
              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">How We Process Your Information</h2>
                
                <div className="bg-blue-50 rounded-lg p-4 mb-4">
                  <h3 className="text-lg font-semibold text-blue-800 mb-2">Stateless Processing</h3>
                  <p className="text-blue-700">
                    All data processing happens in real-time. Your information is processed, used to generate 
                    your CV and cover letter, and then immediately discarded. We operate a completely stateless system.
                  </p>
                </div>

                <h3 className="text-lg font-semibold text-gray-800 mb-3">Processing Steps:</h3>
                <ol className="list-decimal list-inside text-gray-700 space-y-2">
                  <li>You submit your information through our secure web form or file upload</li>
                  <li>Your data is sent via encrypted HTTPS to our processing servers</li>
                  <li>Our AI analyzes and enhances your content</li>
                  <li>Professional CV and cover letter PDFs are generated</li>
                  <li>PDFs are sent back to your browser for download</li>
                  <li>All data is immediately deleted from our servers</li>
                </ol>
              </section>

              {/* Data Retention */}
              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Data Retention</h2>
                
                <div className="bg-green-50 rounded-lg p-4">
                  <h3 className="text-lg font-semibold text-green-800 mb-2">Immediate Deletion</h3>
                  <p className="text-green-700 mb-3">
                    We do not store your personal information, CV content, or generated documents. 
                    All data is processed in memory and deleted immediately after each request is completed.
                  </p>
                  <ul className="list-disc list-inside text-green-700 space-y-1 text-sm">
                    <li><strong>Form Data:</strong> Deleted after PDF generation</li>
                    <li><strong>Uploaded Files:</strong> Deleted after text extraction</li>
                    <li><strong>Generated Content:</strong> Not stored on our servers</li>
                    <li><strong>Log Data:</strong> Basic request logs kept for 30 days for security monitoring</li>
                  </ul>
                </div>
              </section>

              {/* Third-Party Services */}
              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Third-Party Services</h2>
                
                <h3 className="text-lg font-semibold text-gray-800 mb-3">Google Gemini AI</h3>
                <p className="text-gray-700 mb-3">
                  We use Google Gemini AI service to enhance and optimize your CV content. Your data is sent to 
                  Google servers for processing under their privacy policy. Google does not store your data for 
                  training purposes when using our service.
                </p>

                <h3 className="text-lg font-semibold text-gray-800 mb-3">Google Cloud Platform</h3>
                <p className="text-gray-700 mb-3">
                  Our backend services are hosted on Google Cloud Platform in the Europe-West1 region (Belgium) 
                  to ensure GDPR compliance and data locality within the EU.
                </p>

                <h3 className="text-lg font-semibold text-gray-800 mb-3">Vercel</h3>
                <p className="text-gray-700">
                  Our website is hosted on Vercel global edge network. Vercel may collect basic analytics data 
                  such as page views and performance metrics.
                </p>
              </section>

              {/* Your Rights */}
              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Your Rights Under GDPR</h2>
                
                <p className="text-gray-700 mb-4">
                  As we do not store your personal data, most traditional data rights do not apply. However, you have:
                </p>
                
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h4 className="font-semibold text-gray-800 mb-2">Right to Information</h4>
                    <p className="text-gray-600 text-sm">This privacy policy provides full transparency about our data processing.</p>
                  </div>
                  
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h4 className="font-semibold text-gray-800 mb-2">Right to Object</h4>
                    <p className="text-gray-600 text-sm">You can stop using our service at any time without consequence.</p>
                  </div>
                  
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h4 className="font-semibold text-gray-800 mb-2">Right to Complain</h4>
                    <p className="text-gray-600 text-sm">You can lodge a complaint with the Irish Data Protection Commission.</p>
                  </div>
                  
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h4 className="font-semibold text-gray-800 mb-2">Data Portability</h4>
                    <p className="text-gray-600 text-sm">Your generated PDFs are immediately available for download.</p>
                  </div>
                </div>
              </section>

              {/* Security */}
              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Security Measures</h2>
                
                <ul className="space-y-3">
                  <li className="flex items-start">
                    <div className="bg-blue-100 rounded-full p-1 mr-3 mt-1">
                      <Lock className="w-3 h-3 text-blue-600" />
                    </div>
                    <div>
                      <strong className="text-gray-800">HTTPS Encryption:</strong>
                      <span className="text-gray-600"> All data transmission is encrypted using TLS 1.3</span>
                    </div>
                  </li>
                  <li className="flex items-start">
                    <div className="bg-blue-100 rounded-full p-1 mr-3 mt-1">
                      <Shield className="w-3 h-3 text-blue-600" />
                    </div>
                    <div>
                      <strong className="text-gray-800">Rate Limiting:</strong>
                      <span className="text-gray-600"> Protection against abuse and automated attacks</span>
                    </div>
                  </li>
                  <li className="flex items-start">
                    <div className="bg-blue-100 rounded-full p-1 mr-3 mt-1">
                      <Database className="w-3 h-3 text-blue-600" />
                    </div>
                    <div>
                      <strong className="text-gray-800">Memory Processing:</strong>
                      <span className="text-gray-600"> Data processed in memory without persistent storage</span>
                    </div>
                  </li>
                </ul>
              </section>

              {/* Contact */}
              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Contact Information</h2>
                
                <div className="bg-gray-50 rounded-lg p-4">
                  <p className="text-gray-700 mb-3">
                    If you have any questions about this Privacy Policy or our data practices, please contact us.
                  </p>
                  
                  <div className="space-y-2 text-gray-600">
                    <p><strong>Service:</strong> CVGenius</p>
                    <p><strong>Jurisdiction:</strong> Ireland</p>
                    <p><strong>Response Time:</strong> Within 72 hours</p>
                  </div>
                </div>
              </section>

              {/* Governing Law */}
              <section className="border-t pt-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Governing Law</h2>
                
                <p className="text-gray-700">
                  This Privacy Policy is governed by Irish law and EU regulations including the General Data 
                  Protection Regulation (GDPR). Any disputes will be resolved in Irish courts.
                </p>
              </section>
            </div>

            {/* Footer */}
            <div className="text-center mt-8 p-4 bg-white rounded-lg shadow">
              <p className="text-gray-600 text-sm">
                This Privacy Policy is effective as of {new Date().toLocaleDateString('en-IE')} and applies to all users of CVGenius.
              </p>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default PrivacyPolicyPage;