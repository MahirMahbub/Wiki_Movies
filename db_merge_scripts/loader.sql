TRUNCATE TABLE public.data_loader;

INSERT INTO public.data_loader(id, activity_name, status)
VALUES (1, 'Movie Data Loading', True),
       (2, 'Movie Rating Loading', False);