-- Iraq University Platform - Supabase Schema

-- 1. Governorates
CREATE TABLE governorates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name_ar TEXT NOT NULL UNIQUE,
    name_en TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 2. Cities
CREATE TABLE cities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    governorate_id UUID REFERENCES governorates(id) ON DELETE CASCADE,
    name_ar TEXT NOT NULL,
    name_en TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(governorate_id, name_ar)
);

-- 3. Universities
CREATE TABLE universities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    city_id UUID REFERENCES cities(id) ON DELETE SET NULL,
    name_ar TEXT NOT NULL UNIQUE,
    name_en TEXT,
    type TEXT CHECK (type IN ('public', 'private', 'college', 'institute')),
    website_url TEXT,
    description_ar TEXT,
    description_en TEXT,
    logo_url TEXT,
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- 4. Contacts
CREATE TABLE contacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    university_id UUID REFERENCES universities(id) ON DELETE CASCADE,
    label TEXT NOT NULL, -- e.g., 'Registration', 'Head Office'
    phone TEXT,
    email TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 5. Social Links
CREATE TABLE social_links (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    university_id UUID REFERENCES universities(id) ON DELETE CASCADE,
    platform TEXT NOT NULL, -- e.g., 'facebook', 'instagram', 'telegram'
    url TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 6. Posts / News
CREATE TABLE posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    university_id UUID REFERENCES universities(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    content TEXT,
    image_url TEXT,
    published_at TIMESTAMPTZ DEFAULT now(),
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 7. Opportunities (Scholarships, Jobs)
CREATE TABLE opportunities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    university_id UUID REFERENCES universities(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    type TEXT CHECK (type IN ('scholarship', 'job', 'training')),
    deadline DATE,
    url TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 8. Staging (Raw Imports)
CREATE TABLE staging_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_file TEXT,
    raw_data JSONB NOT NULL,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    validation_errors JSONB,
    created_at TIMESTAMPTZ DEFAULT now()
);
