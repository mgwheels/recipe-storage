import { useRef, type FormEvent } from "react";

const API_BASE = "http://127.0.0.1:8000"

export function APITester() {
  const responseInputRef = useRef<HTMLTextAreaElement>(null);
  const payloadRef = useRef<HTMLTextAreaElement>(null);

  const testEndpoint = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      const form = e.currentTarget;
      const formData = new FormData(form);

      // Build payload
      const rawPayload = payloadRef.current?.value?.trim();

      // Build URL
      const path = formData.get("endpoint") as string;
      const fullUrl = path.startsWith("/") ? `${API_BASE}${path}` : `${API_BASE}/${path}`;

      // Identify method and determine support for sending user payload
      const method = formData.get("method") as string;
      const methodsWithBodies = ["POST", "PUT", "PATCH"];
      const shouldSendPayload = methodsWithBodies.includes(method) && rawPayload;

      // Parse and validate user JSON payload
      let parsedPayload;
      if (shouldSendPayload) {
        try {
          parsedPayload = JSON.parse(rawPayload);
        } catch (e) {
          responseInputRef.current!.value = `Invalid JSON payload: ${e}`;
          return; // Stop executing if payload is invalid
        }
      }

      // Update fetch as needed and get res
      const fetchOptions: RequestInit = {
        method,
      };
      if (shouldSendPayload) {
        fetchOptions.headers = { "Content-Type": "application/json" };
        fetchOptions.body = JSON.stringify(parsedPayload)
      }
      const res = await fetch(fullUrl, fetchOptions);

      const data = await res.json();
      responseInputRef.current!.value = JSON.stringify(data, null, 2);
    } catch (error) {
      responseInputRef.current!.value = String(error);
    }
  };

  return (
    <div className="api-tester">
      <form onSubmit={testEndpoint} className="endpoint-row">
        <select name="method" className="method">
          <option value="GET">GET</option>
          <option value="POST">POST</option>
          <option value="PUT">PUT</option>
          <option value="DELETE">DELETE</option>
        </select>
        <input type="text" name="endpoint" defaultValue="/recipes" className="url-input" placeholder="/recipes" />
        <button type="submit" className="send-button">
          Send
        </button>
      </form>
      <textarea
        ref={payloadRef}
        placeholder="Enter JSON payload (for POST/PUT/PATCH methods)"
        className="response-area"
      />
      <textarea
        ref={responseInputRef}
        readOnly
        placeholder="Response will appear here..."
        className="response-area"
      />
    </div>
  );
}
