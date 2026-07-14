const ENV = {
    development: {
        API_BASE_URL: "http://127.0.0.1:8000"
    },
    production: {
        API_BASE_URL: "https://api.plantive.com"
    }
};

// better dev detection
const isLocal =
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1" ||
    window.location.port === "5500";

const currentEnv = isLocal ? "development" : "production";

export const API_BASE_URL = ENV[currentEnv].API_BASE_URL;