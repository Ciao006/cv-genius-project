import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import { User, Mail, Phone, MapPin, Linkedin, Github, Globe } from 'lucide-react';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import { PersonalDetails } from '@/types';

interface Step1Props {
  initialData?: Partial<PersonalDetails>;
  onNext: (data: PersonalDetails) => void;
  onPrevious?: () => void;
  isFirstStep?: boolean;
}

const Step1_Personal: React.FC<Step1Props> = ({
  initialData,
  onNext,
  onPrevious,
  isFirstStep = true
}) => {
  const {
    control,
    handleSubmit,
    formState: { errors, isValid }
  } = useForm<PersonalDetails>({
    defaultValues: {
      full_name: initialData?.full_name || '',
      email: initialData?.email || '',
      phone: initialData?.phone || '',
      linkedin_url: initialData?.linkedin_url || '',
      location: initialData?.location || '',
      github_url: initialData?.github_url || '',
      website_url: initialData?.website_url || '',
    },
    mode: 'onChange'
  });

  const onSubmit = (data: PersonalDetails) => {
    onNext(data);
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Personal Information
        </h2>
        <p className="text-gray-600">
          Let&apos;s start with your basic contact information. This will appear at the top of your CV.
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="md:col-span-2">
            <Controller
              name="full_name"
              control={control}
              rules={{
                required: 'Full name is required',
                minLength: {
                  value: 2,
                  message: 'Name must be at least 2 characters'
                }
              }}
              render={({ field }) => (
                <Input
                  {...field}
                  label="Full Name"
                  placeholder="John Doe"
                  icon={<User className="w-5 h-5" />}
                  error={errors.full_name?.message}
                  required
                />
              )}
            />
          </div>

          <Controller
            name="email"
            control={control}
            rules={{
              required: 'Email address is required',
              pattern: {
                value: /^[^@]+@[^@]+\.[^@]+$/,
                message: 'Please enter a valid email address'
              }
            }}
            render={({ field }) => (
              <Input
                {...field}
                type="email"
                label="Email Address"
                placeholder="john.doe@example.com"
                icon={<Mail className="w-5 h-5" />}
                error={errors.email?.message}
                required
              />
            )}
          />

          <Controller
            name="phone"
            control={control}
            rules={{
              required: 'Phone number is required',
              minLength: {
                value: 5,
                message: 'Phone number must be at least 5 characters'
              },
              pattern: {
                value: /^[+]?[0-9\s\-()]*$/,
                message: 'Phone number can only contain numbers, spaces, hyphens, parentheses, and +'
              }
            }}
            render={({ field: { onChange, ...field } }) => (
              <Input
                {...field}
                type="tel"
                label="Phone Number"
                placeholder="+353 1 234 5678"
                icon={<Phone className="w-5 h-5" />}
                error={errors.phone?.message}
                required
                onChange={(e) => {
                  // Only allow numbers, spaces, hyphens, parentheses, and +
                  const value = e.target.value.replace(/[^+0-9\s\-()]/g, '');
                  onChange(value);
                }}
              />
            )}
          />

          <Controller
            name="location"
            control={control}
            render={({ field }) => (
              <Input
                {...field}
                label="Location"
                placeholder="Dublin, Ireland"
                icon={<MapPin className="w-5 h-5" />}
                error={errors.location?.message}
                helpText="City, Country"
              />
            )}
          />

          <Controller
            name="linkedin_url"
            control={control}
            rules={{
              pattern: {
                value: /^https?:\/\/.*linkedin\.com.*/,
                message: 'Please enter a valid LinkedIn URL'
              }
            }}
            render={({ field }) => (
              <Input
                {...field}
                label="LinkedIn Profile"
                placeholder="https://linkedin.com/in/johndoe"
                icon={<Linkedin className="w-5 h-5" />}
                error={errors.linkedin_url?.message}
                helpText="Optional but recommended"
              />
            )}
          />

          <Controller
            name="github_url"
            control={control}
            rules={{
              pattern: {
                value: /^https?:\/\/.*github\.com.*/,
                message: 'Please enter a valid GitHub URL'
              }
            }}
            render={({ field }) => (
              <Input
                {...field}
                label="GitHub Profile"
                placeholder="https://github.com/johndoe"
                icon={<Github className="w-5 h-5" />}
                error={errors.github_url?.message}
                helpText="Optional - great for technical roles"
              />
            )}
          />

          <Controller
            name="website_url"
            control={control}
            rules={{
              pattern: {
                value: /^https?:\/\/.+\..+/,
                message: 'Please enter a valid website URL'
              }
            }}
            render={({ field }) => (
              <Input
                {...field}
                label="Personal Website"
                placeholder="https://johndoe.com"
                icon={<Globe className="w-5 h-5" />}
                error={errors.website_url?.message}
                helpText="Optional - portfolio, blog, or personal site"
              />
            )}
          />
        </div>

        <div className="flex justify-between pt-6">
          {!isFirstStep && (
            <Button
              type="button"
              variant="secondary"
              onClick={onPrevious}
            >
              Previous
            </Button>
          )}
          
          <Button
            type="submit"
            disabled={!isValid}
            className={isFirstStep ? 'ml-auto' : ''}
          >
            Continue to Work Experience
          </Button>
        </div>
      </form>
    </div>
  );
};

export default Step1_Personal;