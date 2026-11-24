import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import {
  getAuth,
  GoogleAuthProvider,
  signInWithPopup,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  updateProfile,
  sendPasswordResetEmail,
  signOut,
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyCY-xerBTuvjSVkbUzKzyRcyMK5KhYjD3k",
  authDomain: "tcc-dados-deborah.firebaseapp.com",
  projectId: "tcc-dados-deborah",
  appId: "1:401610918602:web:25beeb2ea3c326802d0233",
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
auth.languageCode = "pt-BR";

export function traduzirErroFirebase(code) {
  switch (code) {
    case "auth/invalid-email":
      return "E-mail inválido.";
    case "auth/user-disabled":
      return "Esta conta foi desativada.";
    case "auth/user-not-found":
    case "auth/wrong-password":
    case "auth/invalid-credential":
      return "E-mail ou senha incorretos.";
    case "auth/email-already-in-use":
      return "Já existe uma conta cadastrada com este e-mail.";
    case "auth/weak-password":
      return "A senha deve ter pelo menos 6 caracteres.";
    case "auth/too-many-requests":
      return "Muitas tentativas seguidas. Aguarde um momento e tente novamente.";
    case "auth/popup-closed-by-user":
    case "auth/cancelled-popup-request":
      return "Login com Google cancelado.";
    case "auth/popup-blocked":
      return "O navegador bloqueou o pop-up do Google. Permita pop-ups para este site.";
    case "auth/unauthorized-domain":
      return "Domínio não autorizado no Firebase Authentication. Adicione este domínio nas configurações do Firebase.";
    case "auth/operation-not-allowed":
      return "Este método de login não está ativado no Firebase Authentication.";
    case "auth/network-request-failed":
      return "Falha de conexão. Verifique sua internet e tente novamente.";
    default:
      return "Não foi possível autenticar. Tente novamente.";
  }
}

async function enviarSessaoBackend(endpoint, payload) {
  const response = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  let data = {};
  try {
    data = await response.json();
  } catch {
    throw new Error("Resposta inválida do servidor.");
  }

  if (!response.ok || !data.ok) {
    throw new Error(data.erro || "Não foi possível concluir a autenticação.");
  }
  return data;
}

async function tentarLoginLegado(email, senha, perfil) {
  try {
    const response = await fetch("/auth/legacy-login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, senha, perfil }),
    });
    const data = await response.json();
    if (response.ok && data.ok) {
      return data;
    }
    return null;
  } catch {
    return null;
  }
}

export async function loginComEmailSenha(email, senha, perfil) {
  try {
    const cred = await signInWithEmailAndPassword(auth, email, senha);
    const idToken = await cred.user.getIdToken();
    try {
      return await enviarSessaoBackend("/auth/firebase", {
        idToken,
        perfil,
        acao: "login",
      });
    } catch (backendErr) {
      await signOut(auth).catch(() => {});
      throw backendErr;
    }
  } catch (err) {
    if (err?.code === "auth/invalid-credential" || err?.code === "auth/user-not-found") {
      const legado = await tentarLoginLegado(email, senha, perfil);
      if (legado) return legado;
    }
    if (err?.code) {
      throw new Error(traduzirErroFirebase(err.code));
    }
    throw err;
  }
}

export async function cadastrarComEmailSenha(nome, email, senha, perfil, acceptedTerms = true) {
  try {
    const cred = await createUserWithEmailAndPassword(auth, email, senha);
    await updateProfile(cred.user, { displayName: nome }).catch(() => {});
    const idToken = await cred.user.getIdToken(true);
    try {
      return await enviarSessaoBackend("/auth/firebase", {
        idToken,
        perfil,
        nome,
        accepted_terms: Boolean(acceptedTerms),
        acao: "register",
      });
    } catch (backendErr) {
      await signOut(auth).catch(() => {});
      throw backendErr;
    }
  } catch (err) {
    if (err?.code) {
      throw new Error(traduzirErroFirebase(err.code));
    }
    throw err;
  }
}

export async function entrarComGoogle(perfil, acceptedTerms = true) {
  try {
    const provider = new GoogleAuthProvider();
    provider.setCustomParameters({ prompt: "select_account" });
    const result = await signInWithPopup(auth, provider);
    const idToken = await result.user.getIdToken();
    try {
      return await enviarSessaoBackend("/auth/google", {
        idToken,
        perfil,
        accepted_terms: Boolean(acceptedTerms),
        acao: "google",
      });
    } catch (backendErr) {
      await signOut(auth).catch(() => {});
      throw backendErr;
    }
  } catch (err) {
    if (err?.code) {
      throw new Error(traduzirErroFirebase(err.code));
    }
    throw err;
  }
}

export async function enviarRedefinicaoSenha(email) {
  try {
    await sendPasswordResetEmail(auth, email);
  } catch (err) {
    if (err?.code) {
      throw new Error(traduzirErroFirebase(err.code));
    }
    throw err;
  }
}
