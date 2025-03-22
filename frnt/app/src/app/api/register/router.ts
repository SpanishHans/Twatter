import { NextRequest, NextResponse } from "next/server";
import { registerUser } from "@/app/services/auth/register";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const result = await registerUser(body);  // 🔥 Calls service, not axios directly

    return NextResponse.json(result, { status: 200 });
  } catch (error: any) {
    if (error.response) {
      const { status, data } = error.response;
      return NextResponse.json({ detail: data.detail || "Error" }, { status });
    }

    return NextResponse.json({ detail: "Unknown error" }, { status: 500 });
  }
}
