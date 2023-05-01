from rest_framework import serializers
from . models import User, Hackathon, Submissions


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    #Make passwords hashed
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class HackathonSerializer(serializers.ModelSerializer):
    background_image = serializers.ImageField()
    hackathon_image = serializers.ImageField()

    class Meta:
        model = Hackathon
        fields = ['id', 'title', 'description', 'background_image', 'hackathon_image',
                  'submission_type', 'start_datetime', 'end_datetime', 'reward_prize']


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submissions
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'user', 'hackathon')

    def validate(self, data):
        submission_type = data.get('submission_type')
        if submission_type not in [choice[0] for choice in Submissions.SUBMISSION_TYPES]:
            raise serializers.ValidationError('Invalid submission type')
        if submission_type == 'image' and not data.get('submission_image'):
            raise serializers.ValidationError(
                'Submission image is required for image type')
        if submission_type == 'file' and not data.get('submission_file'):
            raise serializers.ValidationError(
                'Submission file is required for file type')
        if submission_type == 'link' and not data.get('submission_link'):
            raise serializers.ValidationError(
                'Submission link is required for link type')

        if submission_type == 'link' and (data.get('submission_file') or data.get('submission_image')):
            raise serializers.ValidationError('Please Only Submit link')
        if submission_type == 'image' and (data.get('submission_file') or data.get('submission_link')):
            raise serializers.ValidationError('Please Only Submit image')
        if submission_type == 'file' and (data.get('submission_link') or data.get('submission_image')):
            raise serializers.ValidationError('Please only Submit File')

        return data
