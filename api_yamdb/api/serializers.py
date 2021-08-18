from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import (Category, Comment, Genre, Review,  # isort:skip
                            Title)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(
        read_only=True,
        required=False,
        min_value=1,
        max_value=10
    )

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(
        slug_field='slug',
        many=True, queryset=Genre.objects.all()
    )
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.PrimaryKeyRelatedField(read_only=True)
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = self.context['view'].kwargs.get('title_id')
            if Review.objects.filter(
                author=self.context['request'].user, title_id=title_id
            ).exists():
                raise serializers.ValidationError(
                    'User can leave only one review for a title.'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.PrimaryKeyRelatedField(read_only=True)
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
