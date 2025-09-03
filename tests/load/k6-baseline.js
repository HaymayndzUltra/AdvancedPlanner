import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 25,
  duration: '1m',
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<350'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8080/v1';

export default function () {
  const res = http.get(`${BASE_URL}/health`);
  check(res, {
    'status is 200': (r) => r.status === 200,
  });

  // Example: list tasks
  const list = http.get(`${BASE_URL}/tasks?limit=10`);
  check(list, { 'list 200': (r) => r.status === 200 });

  sleep(1);
}