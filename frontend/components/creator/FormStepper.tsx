import React from 'react';
import { Check } from 'lucide-react';
import clsx from 'clsx';

interface Step {
  id: number;
  title: string;
  description: string;
}

interface FormStepperProps {
  steps: Step[];
  currentStep: number;
  completedSteps: number[];
}

const FormStepper: React.FC<FormStepperProps> = ({
  steps,
  currentStep,
  completedSteps
}) => {
  return (
    <div className="mb-8">
      <nav aria-label="Progress">
        <ol className="flex items-center">
          {steps.map((step, index) => {
            const isCompleted = completedSteps.includes(step.id);
            const isCurrent = currentStep === step.id;
            const isLast = index === steps.length - 1;
            
            return (
              <li key={step.id} className={clsx('relative', !isLast && 'pr-8 sm:pr-20')}>
                {/* Connector line */}
                {!isLast && (
                  <div
                    className={clsx(
                      'absolute inset-0 flex items-center',
                      'aria-hidden="true"'
                    )}
                  >
                    <div
                      className={clsx(
                        'h-0.5 w-full',
                        isCompleted ? 'bg-primary-600' : 'bg-gray-200'
                      )}
                    />
                  </div>
                )}
                
                {/* Step indicator */}
                <div className="relative flex items-center justify-center">
                  <div
                    className={clsx(
                      'flex h-8 w-8 items-center justify-center rounded-full text-sm font-medium',
                      isCompleted
                        ? 'bg-primary-600 text-white'
                        : isCurrent
                        ? 'border-2 border-primary-600 bg-white text-primary-600'
                        : 'border-2 border-gray-300 bg-white text-gray-500'
                    )}
                  >
                    {isCompleted ? (
                      <Check className="h-4 w-4" />
                    ) : (
                      <span>{step.id}</span>
                    )}
                  </div>
                  
                  {/* Step title */}
                  <div className="ml-3 hidden sm:block">
                    <p
                      className={clsx(
                        'text-sm font-medium',
                        isCurrent ? 'text-primary-600' : 'text-gray-500'
                      )}
                    >
                      {step.title}
                    </p>
                    <p className="text-xs text-gray-400">{step.description}</p>
                  </div>
                </div>
              </li>
            );
          })}
        </ol>
      </nav>
      
      {/* Mobile step title */}
      <div className="mt-4 sm:hidden">
        <p className="text-sm font-medium text-primary-600">
          Step {currentStep}: {steps.find(s => s.id === currentStep)?.title}
        </p>
        <p className="text-xs text-gray-400">
          {steps.find(s => s.id === currentStep)?.description}
        </p>
      </div>
    </div>
  );
};

export default FormStepper;