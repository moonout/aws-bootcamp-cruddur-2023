INSERT INTO public.users (email, display_name, handle, cognito_user_id)
VALUES
  ('mikro.payne@gmail.com', 'mikro p', 'mikro' ,'MOCK'),
  ('moon.out.of.fog@post.test', 'eugene k', 'moon' ,'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'moon' LIMIT 1),
    'This was imported as seed data! for moon',
    current_timestamp + interval '10 day'
  ),
  (
    (SELECT uuid from public.users WHERE users.handle = 'mikro' LIMIT 1),
    'This was imported as seed data! for mikro',
    current_timestamp + interval '10 day'
  )
;
