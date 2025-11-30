from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import GlobalActivity


@receiver(post_save, sender='metrics.HealthMetrics')
def create_weight_activity(sender, instance, created, **kwargs):
    """Create global activity when weight is logged"""
    if created and hasattr(instance, 'profile') and instance.profile.is_public:
        # Get user's preferred unit
        weight_unit = instance.profile.settings.weight_unit
        if weight_unit == 'kg':
            weight_display = f"{instance.weight_kg:.1f}kg"
        elif weight_unit == 'st':
            stones = int(instance.weight_lb // 14)
            pounds = instance.weight_lb % 14
            weight_display = f"{stones}st {pounds:.0f}lb"
        else:
            weight_display = f"{instance.weight_lb:.1f}lb"
        
        GlobalActivity.objects.create(
            profile=instance.profile,
            activity_type='weight',
            description=f"Logged weight: {weight_display}",
            icon='⚖️',
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id
        )


@receiver(post_save, sender='exercise.ExerciseLog')
def create_exercise_activity(sender, instance, created, **kwargs):
    """Create global activity when exercise is logged"""
    if created and hasattr(instance, 'profile') and instance.profile.is_public:
        description = f"Completed {instance.exercise_type}"
        if instance.duration:
            description += f" for {instance.duration} minutes"
        if hasattr(instance, 'distance') and instance.distance:
            distance_unit = instance.profile.settings.distance_unit
            if distance_unit == 'mi' and hasattr(instance, 'distance_mi'):
                distance_display = f"{instance.distance_mi:.1f}mi"
            else:
                distance_display = f"{instance.distance:.1f}km"
            description += f", {distance_display}"
        
        GlobalActivity.objects.create(
            profile=instance.profile,
            activity_type='exercise',
            description=description,
            icon='🏃',
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id
        )


@receiver(post_save, sender='meals.NutritionLog')
def create_meal_activity(sender, instance, created, **kwargs):
    """Create global activity when meal is logged"""
    if created and hasattr(instance, 'profile') and instance.profile.is_public:
        description = "Logged meal"
        if hasattr(instance, 'meal_name') and instance.meal_name:
            description += f": {instance.meal_name}"
        if hasattr(instance, 'calories') and instance.calories:
            description += f" ({instance.calories} cal)"
        
        GlobalActivity.objects.create(
            profile=instance.profile,
            activity_type='meal',
            description=description,
            icon='🍽️',
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id
        )


@receiver(post_save, sender='milestones.Milestone')
def create_milestone_activity(sender, instance, created, **kwargs):
    """Create global activity when milestone is achieved"""
    if created and hasattr(instance, 'profile') and instance.profile.is_public:
        title = instance.title if hasattr(instance, 'title') else "a milestone"
        description = f"Achieved milestone: {title}"
        
        GlobalActivity.objects.create(
            profile=instance.profile,
            activity_type='milestone',
            description=description,
            icon='🎯',
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id
        )


@receiver(post_save, sender='metrics.Measurement')
def create_measurement_activity(sender, instance, created, **kwargs):
    """Create global activity when body measurement is logged"""
    if created and hasattr(instance, 'profile') and instance.profile.is_public:
        # Build description with available measurements
        parts = []
        if hasattr(instance, 'waist') and instance.waist:
            parts.append(f"waist {instance.waist}cm")
        if hasattr(instance, 'hips') and instance.hips:
            parts.append(f"hips {instance.hips}cm")
        if hasattr(instance, 'chest') and instance.chest:
            parts.append(f"chest {instance.chest}cm")
        
        description = f"Logged measurements: {', '.join(parts)}" if parts else "Logged body measurements"
        
        GlobalActivity.objects.create(
            profile=instance.profile,
            activity_type='measurement',
            description=description,
            icon='📏',
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id
        )
