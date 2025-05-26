// distro-frontend/src/types/index.ts
export interface User {
    id: string;
    email: string;
    employee_id?: string;
    first_name?: string;
    last_name?: string;
    full_name?: string;
    phone_number?: string;
    role: 'admin' | 'supervisor' | 'field_tech' | 'customer_service';
    avatar?: string;
    location_tracking_consent: boolean;
    last_active?: string;
    is_active: boolean;
    permissions: string[];
    date_joined: string;
    last_location?: { lat: number; lng: number; timestamp: string };
    notification_preferences?: Record<string, any>;
    is_deleted?: boolean;
    deleted_on?: string;
    created_by?: string;
    created_by_name?: string;
  }