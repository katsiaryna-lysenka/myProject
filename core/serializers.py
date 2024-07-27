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
    organization = OrganizationSerializer()

    class Meta:
        model = Form2
        fields = '__all__'

    def create(self, validated_data):
        organization_data = validated_data.pop('organization', None)
        if organization_data:
            organizations = Organization.objects.filter(name=organization_data['name'])
            if organizations.exists():
                organization = organizations.first()
                if organizations.count() > 1:
                    print(f"Multiple organizations found with name {organization_data['name']}, using the first one.")
                for attr, value in organization_data.items():
                    setattr(organization, attr, value)
                organization.save()
            else:
                organization = Organization.objects.create(**organization_data)
        else:
            organization = None

        form2_instance = Form2.objects.create(organization=organization, **validated_data)
        return form2_instance

    def update(self, instance, validated_data):
        organization_data = validated_data.pop('organization', None)
        if organization_data:
            org_id = organization_data.get('id')
            if org_id:
                organizations = Organization.objects.filter(id=org_id)
                if organizations.exists():
                    organization = organizations.first()
                    if organizations.count() > 1:
                        print(f"Multiple organizations found with id {org_id}, using the first one.")
                    for attr, value in organization_data.items():
                        setattr(organization, attr, value)
                    organization.save()
                else:
                    organization = Organization.objects.create(**organization_data)
            else:
                organizations = Organization.objects.filter(name=organization_data['name'])
                if organizations.exists():
                    organization = organizations.first()
                    if organizations.count() > 1:
                        print(f"Multiple organizations found with name {organization_data['name']}, using the first one.")
                    for attr, value in organization_data.items():
                        setattr(organization, attr, value)
                    organization.save()
                else:
                    organization = Organization.objects.create(**organization_data)
            instance.organization = organization

        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.save()
        return instance


class Form3Serializer(serializers.ModelSerializer):
    form1 = serializers.PrimaryKeyRelatedField(queryset=Form1.objects.all())
    form2 = serializers.PrimaryKeyRelatedField(queryset=Form2.objects.all())
    modified_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Form3
        fields = '__all__'

    def create(self, validated_data):
        return Form3.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.distribution_count = validated_data.get('distribution_count', instance.distribution_count)
        instance.target_distribution_count = validated_data.get('target_distribution_count',
                                                                instance.target_distribution_count)
        instance.modified_by = validated_data.get('modified_by', instance.modified_by)

        instance.form1 = validated_data.get('form1', instance.form1)
        instance.form2 = validated_data.get('form2', instance.form2)

        instance.save()
        return instance
