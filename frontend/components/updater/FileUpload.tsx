import React, { useCallback, useState } from 'react';
import { useDropzone, FileRejection } from 'react-dropzone';
import { Upload, File, X, AlertCircle, CheckCircle } from 'lucide-react';
import clsx from 'clsx';
import { validateFileSize, validateFileType, formatFileSize } from '@/utils/api';

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  selectedFile: File | null;
  error?: string;
  maxSizeMB?: number;
  allowedTypes?: string[];
}

const FileUpload: React.FC<FileUploadProps> = ({
  onFileSelect,
  selectedFile,
  error,
  maxSizeMB = 5,
  allowedTypes = ['pdf', 'docx', 'doc']
}) => {
  const [dragError, setDragError] = useState<string>('');

  const onDrop = useCallback((acceptedFiles: File[], rejectedFiles: FileRejection[]) => {
    setDragError('');
    
    if (rejectedFiles.length > 0) {
      const rejection = rejectedFiles[0];
      if (rejection.errors[0]?.code === 'file-too-large') {
        setDragError(`File is too large. Maximum size is ${maxSizeMB}MB`);
      } else if (rejection.errors[0]?.code === 'file-invalid-type') {
        setDragError(`Invalid file type. Please upload ${allowedTypes.join(', ').toUpperCase()} files only`);
      } else {
        setDragError('File upload failed. Please try again.');
      }
      return;
    }

    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      
      // Additional validation
      if (!validateFileSize(file, maxSizeMB)) {
        setDragError(`File is too large. Maximum size is ${maxSizeMB}MB`);
        return;
      }
      
      if (!validateFileType(file, allowedTypes)) {
        setDragError(`Invalid file type. Please upload ${allowedTypes.join(', ').toUpperCase()} files only`);
        return;
      }
      
      onFileSelect(file);
    }
  }, [onFileSelect, maxSizeMB, allowedTypes]);

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/msword': ['.doc']
    },
    maxSize: maxSizeMB * 1024 * 1024,
    multiple: false
  });

  const removeFile = () => {
    onFileSelect(null as never);
    setDragError('');
  };

  const currentError = error || dragError;

  return (
    <div className="w-full">
      {!selectedFile ? (
        <div
          {...getRootProps()}
          className={clsx(
            'dropzone cursor-pointer',
            isDragActive && !isDragReject && 'dropzone-active',
            (isDragReject || currentError) && 'dropzone-error'
          )}
        >
          <input {...getInputProps()} />
          
          <div className="flex flex-col items-center">
            <Upload className={clsx(
              'w-12 h-12 mb-4',
              isDragActive ? 'text-primary-500' : 'text-gray-400'
            )} />
            
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              {isDragActive ? 'Drop your CV here' : 'Upload your existing CV'}
            </h3>
            
            <p className="text-sm text-gray-600 mb-4 text-center">
              Drag and drop your CV file here, or click to browse
            </p>
            
            <div className="text-xs text-gray-500 text-center">
              <p>Supported formats: {allowedTypes.map(type => type.toUpperCase()).join(', ')}</p>
              <p>Maximum file size: {maxSizeMB}MB</p>
            </div>
          </div>
        </div>
      ) : (
        <div className="card p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <File className="w-8 h-8 text-primary-600 mr-3" />
              <div>
                <p className="font-medium text-gray-900">{selectedFile.name}</p>
                <p className="text-sm text-gray-500">{formatFileSize(selectedFile.size)}</p>
              </div>
            </div>
            
            <div className="flex items-center">
              <CheckCircle className="w-5 h-5 text-green-500 mr-2" />
              <button
                onClick={removeFile}
                className="p-1 hover:bg-gray-100 rounded-full transition-colors"
                type="button"
              >
                <X className="w-4 h-4 text-gray-500" />
              </button>
            </div>
          </div>
        </div>
      )}
      
      {currentError && (
        <div className="mt-3 flex items-center text-red-600">
          <AlertCircle className="w-4 h-4 mr-2" />
          <span className="text-sm">{currentError}</span>
        </div>
      )}
    </div>
  );
};

export default FileUpload;