class CleanAndSaveFactoryMixin:
    """
    Mixin for a test factory that cleans an instance before saving it.
    """

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Create a model instance, clean it, and save it.

        Args:
            model_class:
                The model class to create an instance of.
            *args:
                The positional arguments to instantiate the model with.
            **kwargs:
                The keyword arguments to instantiate the model with.
        Returns:
            The created model instance.
        """
        instance = model_class(*args, **kwargs)
        instance.clean()
        instance.save()

        return instance
