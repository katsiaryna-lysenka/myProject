from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Organization, UserProfile, Form1, Form2, Form3


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name']


class UserProfileSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'organization']

    def create(self, validated_data):
        organization_data = validated_data.pop('organization')
        organization, created = Organization.objects.get_or_create(**organization_data)
        user_profile = UserProfile.objects.create(organization=organization, **validated_data)
        return user_profile

    def update(self, instance, validated_data):
        organization_data = validated_data.pop('organization')
        organization, created = Organization.objects.get_or_create(**organization_data)

        instance.organization = organization
        instance.user = validated_data.get('user', instance.user)
        instance.save()

        return instance


class Form1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Form1
        fields = '__all__'


class Form2Serializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()  # Nested serializer for organization

    class Meta:
        model = Form2
        fields = '__all__'

    def create(self, validated_data):
        organization_data = validated_data.pop('organization', None)
        if organization_data:
            # Create or update the organization
            organization, created = Organization.objects.update_or_create(
                defaults=organization_data,  # Update if exists or create new
                **organization_data  # Assuming ID is in the data for updating
            )
        else:
            # Handle case where organization is not provided
            organization = None

        form2_instance = Form2.objects.create(organization=organization, **validated_data)
        return form2_instance

    def update(self, instance, validated_data):
        organization_data = validated_data.pop('organization', None)
        if organization_data:
            org_id = organization_data.get('id')
            if org_id:
                # Update existing organization
                organization = Organization.objects.get(id=org_id)
                for attr, value in organization_data.items():
                    setattr(organization, attr, value)
                organization.save()
            else:
                # Create new organization if no id is provided
                organization = Organization.objects.create(**organization_data)
            instance.organization = organization

        # Update other fields
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.save()
        return instance


class Form3Serializer(serializers.ModelSerializer):
    form1 = Form1Serializer()
    form2 = Form2Serializer()

    class Meta:
        model = Form3
        fields = '__all__'

    def create(self, validated_data):
        form1_data = validated_data.pop('form1')
        form2_data = validated_data.pop('form2')

        # Create Form1 instance
        form1_instance = Form1.objects.create(**form1_data)

        # Create Form2 instance
        form2_instance = Form2Serializer().create(form2_data)  # Use Form2Serializer to create Form2

        # Create Form3 instance
        form3_instance = Form3.objects.create(
            form1=form1_instance,
            form2=form2_instance,
            **validated_data
        )

        return form3_instance

    def update(self, instance, validated_data):
        form1_data = validated_data.pop('form1', None)
        form2_data = validated_data.pop('form2', None)

        # Update Form1 instance if provided
        if form1_data:
            form1_instance = instance.form1
            for attr, value in form1_data.items():
                setattr(form1_instance, attr, value)
            form1_instance.save()

        # Update Form2 instance if provided
        if form2_data:
            form2_instance = instance.form2
            Form2Serializer().update(form2_instance, form2_data)  # Use Form2Serializer to update Form2

        # Update Form3 instance fields
        instance.distribution_count = validated_data.get('distribution_count', instance.distribution_count)
        instance.target_distribution_count = validated_data.get('target_distribution_count', instance.target_distribution_count)
        instance.modified_by = validated_data.get('modified_by', instance.modified_by)
        instance.save()

        return instance
