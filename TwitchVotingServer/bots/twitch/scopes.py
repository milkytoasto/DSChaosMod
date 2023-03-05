class Analytics:
    class Read:
        EXTENSIONS = "analytics:read:extensions"
        GAMES = "analytics:read:games"


class Bits:
    READ = "bits:read"


class Channel:
    MODERATE = "channel:moderate"

    class Manage:
        EXTENSIONS = "channel:manage:extensions"
        MODERATORS = "channel:manage:moderators"
        POLLS = "channel:manage:polls"
        PREDICTIONS = "channel:manage:predictions"
        RAIDS = "channel:manage:raids"
        REDEMPTIONS = "channel:manage:redemptions"
        SCHEDULE = "channel:manage:schedule"
        VIDEOS = "channel:manage:videos"
        BROADCAST = "channel:manage:broadcast"
        VIPS = "channel:manage:vips"

    class Edit:
        COMMERCIAL = "channel:edit:commercial"

    class Read:
        CHARITY = "channel:read:charity"
        EDITORS = "channel:read:editors"
        GOALS = "channel:read:goals"
        HYPE_TRAIN = "channel:read:hype_train"
        POLLS = "channel:read:polls"
        PREDICTIONS = "channel:read:predictions"
        REDEMPTIONS = "channel:read:redemptions"
        STREAM_KEY = "channel:read:stream_key"
        SUBSCRIPTIONS = "channel:read:subscriptions"
        VIPS = "channel:read:vips"


class Clips:
    EDIT = "clips:edit"


class Moderation:
    READ = "moderation:read"


class Moderator:
    class Manage:
        ANNOUNCEMENTS = "moderator:manage:announcements"
        AUTOMOD = "moderator:manage:automod"
        AUTOMOD_SETTINGS = "moderator:manage:automod_settings"
        BANNED_USERS = "moderator:manage:banned_users"
        BLOCKED_TERMS = "moderator:manage:blocked_terms"
        CHAT_MESSAGES = "moderator:manage:chat_messages"
        CHAT_SETTINGS = "moderator:manage:chat_settings"
        SHIELD_MODE = "moderator:manage:shield_mode"
        SHOUTOUTS = "moderator:manage:shoutouts"

    class Read:
        BLOCKED_USERS = "moderator:read:blocked_terms"
        CHAT_SETTINGS = "moderator:read:chat_settings"
        CHATTERS = "moderator:read:chatters"
        FOLLOWERS = "moderator:read:followers"
        SHIELD_MODE = "moderator:read:shield_mode"
        SHOUTOUTS = "moderator:read:shoutouts"
        AUTOMOD_SETTINGS = "moderator:read:automod_settings"


class User:
    EDIT = "user:edit"

    class Edit:
        FOLLOWS = "user:edit:follows"

    class Manage:
        BLOCKED_USERS = "user:manage:blocked_users"
        CHAT_COLOR = "user:manage:chat_color"
        WHISPERS = "user:manage:whispers"

    class Read:
        BLOCKED_USERS = "user:read:blocked_users"
        BROADCAST = "user:read:broadcast"
        EMAIL = "user:read:email"
        FOLLOWS = "user:read:follows"
        SUBSCRIPTIONS = "user:read:subscriptions"


class Chat:
    EDIT = "chat:edit"
    READ = "chat:read"


class Whispers:
    EDIT = "whispers:edit"
    READ = "whispers:read"
