import React from 'react';
import { useForm, useFieldArray, Controller } from 'react-hook-form';
import { Plus, Trash2, Briefcase, Calendar, MapPin } from 'lucide-react';
import Input from '@/components/ui/Input';
import Textarea from '@/components/ui/Textarea';
import Button from '@/components/ui/Button';
import { WorkExperience } from '@/types';

interface Step2Props {
  initialData?: WorkExperience[];
  onNext: (data: WorkExperience[]) => void;
  onPrevious: () => void;
}

const Step2_Experience: React.FC<Step2Props> = ({
  initialData,
  onNext,
  onPrevious
}) => {
  const {
    control,
    handleSubmit,
    watch,
    formState: { errors, isValid }
  } = useForm<{ experiences: WorkExperience[] }>({
    defaultValues: {
      experiences: initialData?.length ? initialData : [{
        job_title: '',
        company: '',
        start_date: '',
        end_date: '',
        is_current: false,
        description: '',
        location: ''
      }]
    },
    mode: 'onChange'
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'experiences'
  });

  const watchedExperiences = watch('experiences');

  const onSubmit = (data: { experiences: WorkExperience[] }) => {
    const validExperiences = data.experiences.filter(exp => 
      exp.job_title.trim() && exp.company.trim() && exp.description.trim()
    );
    onNext(validExperiences);
  };

  const addExperience = () => {
    append({
      job_title: '',
      company: '',
      start_date: '',
      end_date: '',
      is_current: false,
      description: '',
      location: ''
    });
  };

  const removeExperience = (index: number) => {
    if (fields.length > 1) {
      remove(index);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Work Experience
        </h2>
        <p className="text-gray-600">
          Add your work experience, starting with your most recent position. 
          Include brief notes about your responsibilities - our AI will transform them into professional bullet points.
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
        {fields.map((field, index) => (
          <div key={field.id} className="card p-6 relative">
            {/* Remove button */}
            {fields.length > 1 && (
              <button
                type="button"
                onClick={() => removeExperience(index)}
                className="absolute top-4 right-4 p-2 text-gray-400 hover:text-red-500 transition-colors"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            )}

            <div className="flex items-center mb-4">
              <Briefcase className="w-5 h-5 text-primary-600 mr-2" />
              <h3 className="text-lg font-semibold text-gray-900">
                Experience {index + 1}
              </h3>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <Controller
                name={`experiences.${index}.job_title`}
                control={control}
                rules={{
                  required: 'Job title is required',
                  minLength: {
                    value: 2,
                    message: 'Job title must be at least 2 characters'
                  }
                }}
                render={({ field }) => (
                  <Input
                    {...field}
                    label="Job Title"
                    placeholder="Software Engineer"
                    error={errors.experiences?.[index]?.job_title?.message}
                    required
                  />
                )}
              />

              <Controller
                name={`experiences.${index}.company`}
                control={control}
                rules={{
                  required: 'Company name is required',
                  minLength: {
                    value: 2,
                    message: 'Company name must be at least 2 characters'
                  }
                }}
                render={({ field }) => (
                  <Input
                    {...field}
                    label="Company"
                    placeholder="Tech Corp Ltd"
                    error={errors.experiences?.[index]?.company?.message}
                    required
                  />
                )}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <Controller
                name={`experiences.${index}.start_date`}
                control={control}
                rules={{
                  required: 'Start date is required'
                }}
                render={({ field }) => (
                  <Input
                    {...field}
                    label="Start Date"
                    placeholder="Jan 2020"
                    icon={<Calendar className="w-4 h-4" />}
                    error={errors.experiences?.[index]?.start_date?.message}
                    required
                    helpText="e.g., Jan 2020, March 2021"
                  />
                )}
              />

              <Controller
                name={`experiences.${index}.end_date`}
                control={control}
                render={({ field }) => (
                  <Input
                    {...field}
                    label="End Date"
                    placeholder="Dec 2023"
                    icon={<Calendar className="w-4 h-4" />}
                    error={errors.experiences?.[index]?.end_date?.message}
                    disabled={watchedExperiences[index]?.is_current}
                    helpText={watchedExperiences[index]?.is_current ? "Current position" : "e.g., Dec 2023, Present"}
                  />
                )}
              />

              <div className="flex items-center pt-8">
                <Controller
                  name={`experiences.${index}.is_current`}
                  control={control}
                  render={({ field }) => (
                    <label className="flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        checked={field.value}
                        onChange={(e) => {
                          field.onChange(e.target.checked);
                          if (e.target.checked) {
                            // Clear end date when current is checked
                            const currentData = watchedExperiences[index];
                            if (currentData) {
                              currentData.end_date = '';
                            }
                          }
                        }}
                        className="w-4 h-4 text-primary-600 bg-gray-100 border-gray-300 rounded focus:ring-primary-500 focus:ring-2"
                      />
                      <span className="ml-2 text-sm text-gray-700">Current position</span>
                    </label>
                  )}
                />
              </div>
            </div>

            <div className="mb-4">
              <Controller
                name={`experiences.${index}.location`}
                control={control}
                render={({ field }) => (
                  <Input
                    {...field}
                    label="Location"
                    placeholder="Dublin, Ireland"
                    icon={<MapPin className="w-4 h-4" />}
                    error={errors.experiences?.[index]?.location?.message}
                    helpText="Optional - City, Country"
                  />
                )}
              />
            </div>

            <Controller
              name={`experiences.${index}.description`}
              control={control}
              rules={{
                required: 'Job description is required',
                minLength: {
                  value: 10,
                  message: 'Description must be at least 10 characters'
                }
              }}
              render={({ field }) => (
                <Textarea
                  {...field}
                  label="Responsibilities & Achievements"
                  placeholder="Describe your key responsibilities and achievements. Use bullet points or short sentences. Our AI will enhance this into professional content."
                  error={errors.experiences?.[index]?.description?.message}
                  rows={4}
                  required
                  helpText="Tip: Include specific technologies, metrics, and accomplishments"
                />
              )}
            />
          </div>
        ))}

        {/* Add Experience Button */}
        <div className="text-center">
          <Button
            type="button"
            onClick={addExperience}
            variant="outline"
            icon={<Plus className="w-4 h-4" />}
          >
            Add Another Experience
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
            Continue to Education
          </Button>
        </div>
      </form>
    </div>
  );
};

export default Step2_Experience;