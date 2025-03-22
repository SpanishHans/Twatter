import axios from "axios";

// Common headers
const defaultHeaders = {
  "Content-Type": "application/json",
};

// Factory function for DRY creation
const createAxiosInstance = (baseURL: string) => {
  const instance = axios.create({
    baseURL,
    headers: defaultHeaders,
    withCredentials: true,  // Sends cookies for auth
  });

  // --- Interceptors ---

  // Request interceptor – logs all outgoing requests
  instance.interceptors.request.use(
    (config) => {
      console.log(`[Request] ${config.method?.toUpperCase()} ${config.url}`);
      return config;
    },
    (error) => {
      console.error("[Request Error]", error);
      return Promise.reject(error);
    }
  );

  // Response interceptor – handles responses & errors
  instance.interceptors.response.use(
    (response) => {
      return response;
    },
    (error) => {
      if (error.response) {
        const status = error.response.status;
        const url = error.response.config.url;
        console.error(`[Response Error] ${status} ${url}`);

        if (status === 401) {
          console.warn("Unauthorized (401) – consider redirecting to login.");
          // Example: redirect to login (uncomment if needed)
          // if (typeof window !== 'undefined') {
          //   window.location.href = "/login";
          // }
        }
      } else {
        console.error("[Response Error] No response from server", error);
      }

      return Promise.reject(error);
    }
  );

  return instance;
};

// Create axios instances for your services
const axiosAuth = createAxiosInstance(
  process.env.NEXT_AUTH_API_BASE_URL || "http://twatter_auth:8000"
);

const axiosPubs = createAxiosInstance(
  process.env.NEXT_PUBS_API_BASE_URL || "http://twatter_pubs:8000"
);

const axiosInts = createAxiosInstance(
  process.env.NEXT_INTS_API_BASE_URL || "http://twatter_ints:8000"
);

export { axiosAuth, axiosPubs, axiosInts };
