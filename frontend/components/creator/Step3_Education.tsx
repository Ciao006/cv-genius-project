import React from 'react';
import { useForm, useFieldArray, Controller } from 'react-hook-form';
import { Plus, Trash2, GraduationCap, Calendar, MapPin } from 'lucide-react';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import { Education } from '@/types';

interface Step3Props {
  initialData?: Education[];
  onNext: (data: Education[]) => void;
  onPrevious: () => void;
}

const Step3_Education: React.FC<Step3Props> = ({
  initialData,
  onNext,
  onPrevious
}) => {
  const {
    control,
    handleSubmit,
    formState: { errors, isValid }
  } = useForm<{ education: Education[] }>({
    defaultValues: {
      education: initialData?.length ? initialData : [{
        degree: '',
        institution: '',
        start_date: '',
        end_date: '',
        grade: '',
        location: ''
      }]
    },
    mode: 'onChange'
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'education'
  });

  const onSubmit = (data: { education: Education[] }) => {
    const validEducation = data.education.filter(edu => 
      edu.degree.trim() && edu.institution.trim()
    );
    
    // Backend requires at least 1 education entry
    if (validEducation.length === 0) {
      // Add a default education entry if none exist
      validEducation.push({
        degree: 'Not specified',
        institution: 'Not specified',
        start_date: '2020',
        end_date: '2024',
        grade: '',
        location: ''
      });
    }
    
    onNext(validEducation);
  };

  const addEducation = () => {
    append({
      degree: '',
      institution: '',
      start_date: '',
      end_date: '',
      grade: '',
      location: ''
    });
  };

  const removeEducation = (index: number) => {
    if (fields.length > 1) {
      remove(index);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Education
        </h2>
        <p className="text-gray-600">
          Add your educational background, starting with your highest qualification. 
          Include degrees, certifications, and relevant training programs.
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
        {fields.map((field, index) => (
          <div key={field.id} className="card p-6 relative">
            {/* Remove button */}
            {fields.length > 1 && (
              <button
                type="button"
                onClick={() => removeEducation(index)}
                className="absolute top-4 right-4 p-2 text-gray-400 hover:text-red-500 transition-colors"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            )}

            <div className="flex items-center mb-4">
              <GraduationCap className="w-5 h-5 text-primary-600 mr-2" />
              <h3 className="text-lg font-semibold text-gray-900">
                Education {index + 1}
              </h3>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <Controller
                name={`education.${index}.degree`}
                control={control}
                rules={{
                  required: 'Degree/Qualification is required',
                  minLength: {
                    value: 2,
                    message: 'Degree must be at least 2 characters'
                  }
                }}
                render={({ field }) => (
                  <Input
                    {...field}
                    label="Degree/Qualification"
                    placeholder="BSc Computer Science"
                    error={errors.education?.[index]?.degree?.message}
                    required
                    helpText="e.g., BSc, MSc, PhD, Certificate"
                  />
                )}
              />

              <Controller
                name={`education.${index}.institution`}
                control={control}
                rules={{
                  required: 'Institution name is required',
                  minLength: {
                    value: 2,
                    message: 'Institution name must be at least 2 characters'
                  }
                }}
                render={({ field }) => (
                  <Input
                    {...field}
                    label="Institution"
                    placeholder="Trinity College Dublin"
                    error={errors.education?.[index]?.institution?.message}
                    required
                  />
                )}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <Controller
                name={`education.${index}.start_date`}
                control={control}
                rules={{
                  required: 'Start date is required'
                }}
                render={({ field }) => (
                  <Input
                    {...field}
                    label="Start Date"
                    placeholder="Sep 2016"
                    icon={<Calendar className="w-4 h-4" />}
                    error={errors.education?.[index]?.start_date?.message}
                    required
                    helpText="e.g., Sep 2016, January 2020"
                  />
                )}
              />

              <Controller
                name={`education.${index}.end_date`}
                control={control}
                render={({ field }) => (
                  <Input
                    {...field}
                    label="End Date"
                    placeholder="Jun 2020"
                    icon={<Calendar className="w-4 h-4" />}
                    error={errors.education?.[index]?.end_date?.message}
                    helpText="Leave blank if ongoing"
                  />
                )}
              />

              <Controller
                name={`education.${index}.grade`}
                control={control}
                render={({ field }) => (
                  <Input
                    {...field}
                    label="Grade/Result"
                    placeholder="First Class Honours"
                    error={errors.education?.[index]?.grade?.message}
                    helpText="e.g., First Class, 3.8 GPA, Distinction"
                  />
                )}
              />
            </div>

            <div className="mb-4">
              <Controller
                name={`education.${index}.location`}
                control={control}
                render={({ field }) => (
                  <Input
                    {...field}
                    label="Location"
                    placeholder="Dublin, Ireland"
                    icon={<MapPin className="w-4 h-4" />}
                    error={errors.education?.[index]?.location?.message}
                    helpText="Optional - City, Country"
                  />
                )}
              />
            </div>
          </div>
        ))}

        {/* Add Education Button */}
        <div className="text-center">
          <Button
            type="button"
            onClick={addEducation}
            variant="outline"
            icon={<Plus className="w-4 h-4" />}
          >
            Add Another Qualification
          </Button>
        </div>

        {/* Navigation Buttons */}
        <div className="flex justify-between pt-6">
          <Button
            type="button"
            variant="secondary"
            onClick={onPrevious}
          >
            Previous
          </Button>
          
          <Button
            type="submit"
            disabled={!isValid || fields.length === 0}
          >
            Continue to Skills
          </Button>
        </div>
      </form>
    </div>
  );
};

export default Step3_Education;