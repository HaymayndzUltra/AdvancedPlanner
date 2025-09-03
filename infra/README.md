Infra overview

- Base manifests in `infra/base` using Argo Rollouts for progressive delivery.
- Environment overlays in `infra/overlays/{staging,production}` via Kustomize.
- Replace `ghcr.io/${REPO}/${APP_IMAGE_SHA}` at deploy time with the built image.

Requirements

- Kubernetes cluster with Argo Rollouts controller and NGINX Ingress
- kubectl, kustomize (or kubectl kustomize), and argo-rollouts plugin

