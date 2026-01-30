# Feature Specification: Interface de Prédiction de Gravité d'Accidents

**Feature Branch**: `001-streamlit-prediction-ui`
**Created**: 2026-01-30
**Status**: Draft
**Input**: User description: "Créer une interface Streamlit pour prédire la gravité des accidents"

## User Scenarios & Testing *(mandatory)*

### EPIC 1 — Parcours de saisie multi-pages (menus déroulants)

**Objectif**: L'utilisateur renseigne 15 champs, répartis sur plusieurs pages, sans confusion.

#### US-01 — Démarrer une nouvelle prédiction (Priority: P1)

**En tant que** utilisateur
**Je veux** commencer une nouvelle prédiction via un bouton "Nouvelle prédiction"
**Afin de** saisir progressivement les informations de l'accident.

**Why this priority**: Point d'entrée fondamental pour toute utilisation de l'interface. Bloquant pour le MVP.

**Independent Test**: L'utilisateur peut cliquer sur "Nouvelle prédiction" et voir le formulaire se réinitialiser complètement avec un indicateur de progression. Testable indépendamment des autres fonctionnalités.

**Acceptance Scenarios**:

1. **Given** l'utilisateur est sur l'interface, **When** il clique sur "Nouvelle prédiction", **Then** toutes les sélections précédentes sont réinitialisées

2. **Given** le formulaire est réinitialisé, **When** l'utilisateur consulte l'interface, **Then** un indicateur de progression affiche "Page 1/6"

---

#### US-02 — Saisie multi-pages claire (avec navigation) (Priority: P1)

**En tant que** utilisateur
**Je veux** un formulaire en plusieurs pages clairement regroupées
**Afin de** ne pas être noyé dans 15 critères.

**Why this priority**: Expérience utilisateur critique - 15 champs sur une seule page serait écrasant. Essentiel pour l'utilisabilité.

**Independent Test**: L'utilisateur peut naviguer entre les 6 pages avec les boutons Précédent/Suivant, et voir les champs regroupés logiquement. Testable via navigation sans soumission.

**Structure des pages** (recommandée):
- **Page 1 — Contexte & route**: dep, agg, catr, vma_bucket
- **Page 2 — Infrastructure**: int, circ
- **Page 3 — Collision**: col, choc_mode, manv_mode
- **Page 4 — Conducteur**: driver_age_bucket, driver_trajet_family
- **Page 5 — Conditions & tranche horaire**: lum, atm, time_bucket
- **Page 6 — Récap & prédiction**: résumé + bouton "Prédire"

**Acceptance Scenarios**:

1. **Given** l'utilisateur est sur une page du formulaire, **When** il clique sur "Suivant", **Then** il accède à la page suivante et ses sélections sont préservées

2. **Given** l'utilisateur est sur la page 3, **When** il clique sur "Précédent", **Then** il revient à la page 2 avec ses sélections intactes

3. **Given** l'utilisateur consulte n'importe quelle page, **When** il observe les champs, **Then** tous sont affichés sous forme de menus déroulants verticaux (un par ligne)

4. **Given** l'utilisateur est sur n'importe quelle page, **When** il cherche un champ de saisie texte libre, **Then** il n'en trouve aucun (sauf recherche interne dans liste longue pour dep)

---

#### US-03 — Chaque menu affiche "Code + Libellé" (référentiel) (Priority: P1)

**En tant que** utilisateur
**Je veux** voir le code + le libellé dans les choix (ex: "1 — Plein jour")
**Afin de** sélectionner sans ambiguïté et respecter le data dictionary.

**Why this priority**: Garantit la conformité avec le dictionnaire de données et évite les erreurs de saisie. Essentiel pour la qualité des données.

**Independent Test**: L'utilisateur peut ouvrir n'importe quel menu déroulant et voir que chaque option affiche le format "code — libellé". Testable champ par champ.

**Acceptance Scenarios**:

1. **Given** l'utilisateur ouvre le menu déroulant pour "lum", **When** il consulte les options, **Then** il voit "1 — Plein jour", "2 — Crépuscule ou aube", etc.

2. **Given** l'utilisateur est sur un champ quelconque, **When** il clique sur le lien "Voir le référentiel", **Then** une aide (modal ou panneau latéral) s'ouvre montrant la table complète des codes pour ce champ

---

#### US-04 — Gestion des valeurs "Non renseigné" (Priority: P2)

**En tant que** utilisateur
**Je veux** pouvoir choisir "Non renseigné / Inconnu" quand je ne sais pas
**Afin de** quand même obtenir une prédiction.

**Why this priority**: Améliore la flexibilité - permet d'obtenir une prédiction même avec données incomplètes. Important mais pas bloquant pour le MVP.

**Independent Test**: L'utilisateur peut sélectionner "Non renseigné" pour des champs spécifiques et voir que l'API reçoit la valeur appropriée selon le référentiel.

**Acceptance Scenarios**:

1. **Given** l'utilisateur ouvre un menu déroulant pour un champ catégoriel, **When** il consulte les options, **Then** il voit une option "Non renseigné / Inconnu" si prévu au référentiel (ex: -1 ou "unknown")

2. **Given** l'utilisateur sélectionne "Non renseigné" pour "atm", **When** il soumet le formulaire, **Then** l'API reçoit la valeur -1 selon le mapping défini

---

### EPIC 2 — Validation et cohérence avant prédiction

**Objectif**: Garantir que seules des données valides atteignent l'API de prédiction.

#### US-05 — Validation "15 champs requis" (Priority: P1)

**En tant que** utilisateur
**Je veux** être bloqué si un champ requis n'est pas renseigné
**Afin d'** éviter des requêtes invalides.

**Why this priority**: Prévient les erreurs API et garantit la qualité des prédictions. Critique pour la robustesse du système.

**Independent Test**: L'utilisateur peut tenter de soumettre avec des champs vides et voir le système bloquer la soumission avec un message clair.

**Acceptance Scenarios**:

1. **Given** l'utilisateur n'a pas rempli tous les 15 champs, **When** il arrive sur la page "Récap & prédiction", **Then** le bouton "Prédire" est désactivé

2. **Given** le bouton "Prédire" est désactivé, **When** l'utilisateur consulte l'interface, **Then** un message indique clairement les champs manquants (ex: "Page 2 - Infrastructure: circ non renseigné")

3. **Given** l'utilisateur a rempli tous les 15 champs, **When** il arrive sur la page récap, **Then** le bouton "Prédire" devient actif

---

#### US-06 — Validation de time_bucket sans saisie libre (Priority: P1)

**En tant que** utilisateur
**Je veux** choisir une tranche horaire dans une liste simple
**Afin de** rester stable et éviter les erreurs de format.

**Why this priority**: Évite les erreurs de format courantes. Garantit la conformité avec un champ catégoriel stable.

**Independent Test**: L'utilisateur peut sélectionner une tranche horaire via dropdown uniquement, sans possibilité de saisie libre.

**Acceptance Scenarios**:

1. **Given** l'utilisateur est sur la page "Conditions & tranche horaire", **When** il consulte le champ "time_bucket", **Then** il voit un dropdown avec les valeurs `night_00_05`, `morning_06_11`, `afternoon_12_17`, `evening_18_23`

2. **Given** l'utilisateur tente de saisir du texte dans le champ time_bucket, **When** il essaie, **Then** aucune saisie texte libre n'est possible (seulement sélection via dropdown)

---

### EPIC 3 — Prédiction et affichage du résultat

**Objectif**: Fournir une prédiction claire et interprétable à l'utilisateur.

#### US-07 — Obtenir la probabilité + la classe (seuil fixé à 0.47) (Priority: P1)

**En tant que** utilisateur
**Je veux** voir la probabilité d'accident grave + la classe finale
**Afin de** comprendre le résultat.

**Why this priority**: Cœur de la fonctionnalité - raison d'être de l'interface. Absolument critique pour le MVP.

**Independent Test**: L'utilisateur peut soumettre un formulaire complet et voir s'afficher la probabilité (0-1) et le label (grave/non-grave) selon la règle de seuil 0.47.

**Acceptance Scenarios**:

1. **Given** l'utilisateur a rempli tous les champs et clique sur "Prédire", **When** l'API retourne une probabilité de 0.65, **Then** l'interface affiche "proba: 0.65" et "classe: grave" (car 0.65 ≥ 0.47)

2. **Given** l'utilisateur soumet une prédiction, **When** l'API retourne une probabilité de 0.32, **Then** l'interface affiche "proba: 0.32" et "classe: non_grave" (car 0.32 < 0.47)

3. **Given** l'utilisateur consulte le résultat, **When** il lit l'affichage, **Then** il voit clairement le seuil appliqué (threshold = 0.47) et la règle de décision

---

#### US-08 — Voir un récapitulatif des 15 champs envoyés (Priority: P2)

**En tant que** utilisateur
**Je veux** voir un tableau récapitulatif (champ / code / libellé)
**Afin de** vérifier avant d'envoyer.

**Why this priority**: Permet la vérification finale avant soumission. Améliore la confiance mais pas bloquant pour la fonctionnalité de base.

**Independent Test**: L'utilisateur peut accéder à la page 6 (Récap) et voir tous ses choix résumés dans un tableau clair.

**Acceptance Scenarios**:

1. **Given** l'utilisateur arrive sur la page 6 "Récap & prédiction", **When** il consulte la page, **Then** il voit un tableau avec 15 lignes affichant : nom du champ | code sélectionné | libellé correspondant

2. **Given** l'utilisateur consulte le récap et détecte une erreur, **When** il clique sur "Précédent", **Then** il peut retourner aux pages précédentes pour corriger ses choix

---

### EPIC 4 — Référentiel intégré (data dictionary product15)

**Objectif**: Intégrer le dictionnaire de données comme source de vérité pour les options et l'aide contextuelle.

#### US-09 — Aide contextuelle par champ (Priority: P2)

**En tant que** utilisateur
**Je veux** une aide ("i") à côté de chaque champ
**Afin de** comprendre sa signification.

**Why this priority**: Facilite l'adoption par les utilisateurs non-experts. Important pour l'accessibilité mais pas bloquant pour le MVP.

**Independent Test**: L'utilisateur peut cliquer sur l'icône d'aide de n'importe quel champ et voir une aide contextuelle complète.

**Acceptance Scenarios**:

1. **Given** l'utilisateur voit un champ quelconque, **When** il clique sur l'icône "i" à côté du champ, **Then** l'aide affiche une définition courte du champ

2. **Given** l'aide contextuelle est affichée, **When** l'utilisateur la consulte, **Then** il voit la table complète des codes (ou la liste de valeurs possibles si bucket/string)

3. **Given** l'utilisateur consulte l'aide pour "manv_mode", **When** il lit le contenu, **Then** il voit des exemples de manœuvres courantes avec leurs codes

---

#### US-10 — Référentiel "source de vérité" centralisé (Priority: P3)

**En tant que** PO/Dev
**Je veux** que l'UI charge les options depuis un JSON unique (meta/ref)
**Afin de** garantir la conformité au modèle.

**Why this priority**: Architecture technique qui améliore la maintenabilité. Utile mais peut être implémenté progressivement après le MVP.

**Independent Test**: Le développeur peut vérifier que les options de menus déroulants sont chargées depuis un fichier JSON centralisé plutôt que hardcodées.

**Acceptance Scenarios**:

1. **Given** le système démarre, **When** l'interface se charge, **Then** les listes d'options sont lues depuis un fichier `meta/ref.json` ou `catboost_product15_meta.json` + `ref_options.json`

2. **Given** le modèle évolue avec de nouveaux codes, **When** le fichier meta/ref.json est mis à jour, **Then** l'interface reflète automatiquement les changements sans modification du code front

---

### EPIC 5 — Non-fonctionnel (qualité, accessibilité, logs)

**Objectif**: Garantir la qualité, l'accessibilité, et l'observabilité de l'interface.

#### US-11 — Accessibilité et mobile-first (Priority: P2)

**En tant que** utilisateur mobile
**Je veux** des menus déroulants utilisables au pouce
**Afin de** compléter le formulaire facilement.

**Why this priority**: Étend l'accessibilité aux utilisateurs mobiles. Important pour l'adoption mais non-bloquant si l'on cible prioritairement desktop/tablette.

**Independent Test**: L'utilisateur peut ouvrir l'interface sur mobile et utiliser les menus déroulants confortablement.

**Acceptance Scenarios**:

1. **Given** l'utilisateur accède à l'interface sur mobile, **When** il ouvre un menu déroulant, **Then** les options sont affichées avec une taille suffisamment grande pour être tapées au pouce

2. **Given** l'utilisateur sur mobile fait défiler une liste longue (ex: dep), **When** il scrolle, **Then** le scroll est fluide et les options restent lisibles

3. **Given** l'utilisateur consulte l'interface sur mobile, **When** il observe les labels et boutons, **Then** le contraste est suffisant et les labels sont explicites

---

#### US-12 — Observabilité minimale (Priority: P3)

**En tant que** développeur
**Je veux** des logs des requêtes (sans données personnelles)
**Afin de** diagnostiquer les erreurs.

**Why this priority**: Aide au debugging et monitoring en production. Utile mais pas critique pour le lancement initial.

**Independent Test**: Le développeur peut consulter les logs et voir les informations de requête sans données utilisateur sensibles.

**Acceptance Scenarios**:

1. **Given** une requête de prédiction est effectuée, **When** le système traite la requête, **Then** un log est créé avec : timestamp, statut HTTP, temps de réponse, version du modèle

2. **Given** les logs sont consultés, **When** le développeur les inspecte, **Then** aucune donnée de saisie utilisateur n'est stockée par défaut (conformité RGPD)

---

### Edge Cases

- **Que se passe-t-il quand** l'API backend est indisponible ou ne répond pas dans un délai raisonnable (>10 secondes) ?
  → L'interface affiche un message d'erreur clair et actionnable (ex: "Service temporairement indisponible, veuillez réessayer")

- **Que se passe-t-il quand** l'utilisateur saisit une combinaison de variables jamais vue dans les données d'entraînement (ex: département inconnu + conditions extrêmes) ?
  → Le modèle produit quand même une prédiction (comportement CatBoost), mais l'interface peut afficher un avertissement sur le niveau de confiance

- **Que se passe-t-il quand** l'utilisateur navigue entre les pages sans sauvegarder ?
  → Les sélections sont préservées en mémoire (session state) jusqu'à la réinitialisation explicite via "Nouvelle prédiction"

- **Que se passe-t-il quand** l'utilisateur ferme le navigateur au milieu d'une saisie ?
  → Les données non soumises sont perdues (pas de persistance) - comportement attendu pour une interface publique/anonyme

- **Que se passe-t-il quand** le champ "dep" (107 codes) est affiché sur mobile ?
  → Un champ de recherche/filtrage dans le dropdown est fourni pour trouver rapidement le département souhaité

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: L'interface DOIT organiser la saisie des 15 variables en 6 pages thématiques (Contexte & route, Infrastructure, Collision, Conducteur, Conditions & tranche horaire, Récap)

- **FR-002**: L'interface DOIT fournir des boutons de navigation "Précédent" et "Suivant" entre les pages

- **FR-003**: L'interface DOIT afficher un indicateur de progression "Page X/6" sur chaque page

- **FR-004**: Tous les champs DOIVENT être des menus déroulants (pas de saisie texte libre sauf recherche interne pour dep)

- **FR-005**: Chaque option de menu déroulant DOIT afficher le format "code — libellé" (ex: "1 — Plein jour")

- **FR-006**: Les champs supportant "Non renseigné" DOIVENT inclure une option "-1 — Non renseigné" ou "unknown"

- **FR-007**: Le bouton "Prédire" DOIT être désactivé tant que les 15 champs ne sont pas remplis

- **FR-008**: Un message DOIT indiquer clairement les champs manquants avec leur page de localisation

- **FR-009**: Le champ "time_bucket" DOIT être un dropdown (night_00_05, morning_06_11, afternoon_12_17, evening_18_23)

- **FR-010**: La page 6 "Récap" DOIT afficher un tableau récapitulatif des 15 choix (champ | code | libellé)

- **FR-011**: L'interface DOIT afficher le résultat avec : probabilité (0-1), classe (grave/non-grave), seuil appliqué (0.47)

- **FR-012**: Chaque champ DOIT avoir une icône "i" ouvrant une aide contextuelle avec définition et table des codes

- **FR-013**: Les options des menus déroulants DOIVENT être chargées depuis un fichier JSON centralisé (meta/ref)

- **FR-014**: Un bouton "Nouvelle prédiction" DOIT réinitialiser complètement le formulaire

- **FR-015**: Les requêtes à l'API DOIVENT être loggées avec timestamp, statut, temps de réponse, version modèle (sans données utilisateur)

### Key Entities

- **Session de Prédiction**: Représente une séquence de saisie multi-pages avec état préservé entre les pages jusqu'à soumission ou réinitialisation

- **Page de Formulaire**: Une des 6 pages thématiques contenant un sous-ensemble des 15 variables

- **Référentiel de Codes**: Fichier JSON centralisé contenant tous les codes BAAC et libellés pour chaque variable

- **Résultat de Prédiction**: Objet contenant la probabilité brute (0-1), la classe finale (grave/non-grave), le seuil appliqué (0.47), et le récapitulatif des 15 variables d'entrée

### UI/UX Requirements

**Input Collection**:
- **UIX-001**: L'interface DOIT présenter les 15 variables réparties sur 6 pages thématiques selon la structure définie (US-02)

- **UIX-002**: Tous les champs DOIVENT être des menus déroulants verticaux (un par ligne)

- **UIX-003**: Les options DOIVENT afficher "code — libellé" en français (ex: "1 — Plein jour")

- **UIX-004**: Le champ "dep" DOIT inclure une fonction de recherche/filtrage pour les 107 départements

**User Guidance**:
- **UIX-005**: Chaque champ DOIT avoir une icône "i" cliquable

- **UIX-006**: L'aide contextuelle DOIT afficher : définition courte + table complète des codes/catégories

- **UIX-007**: Un lien "Voir le référentiel" DOIT ouvrir une aide (modal/panneau latéral) par champ

- **UIX-008**: Les messages d'erreur DOIVENT être clairs et actionnables avec localisation précise (page + champ)

**User Experience**:
- **UIX-009**: Un indicateur de progression "Page X/6" DOIT être affiché en permanence

- **UIX-010**: Les boutons "Précédent" et "Suivant" DOIVENT être accessibles et clairement visibles

- **UIX-011**: Les sélections DOIVENT être préservées lors de la navigation entre pages

- **UIX-012**: La page 6 "Récap" DOIT afficher un tableau récapitulatif avant soumission

- **UIX-013**: Le bouton "Prédire" DOIT être désactivé visuellement (grisé) si champs manquants

- **UIX-014**: Le résultat DOIT être affiché avec code couleur visuel (rouge=grave, vert=non-grave)

**Accessibility**:
- **UIX-015**: Les menus déroulants DOIVENT être utilisables au pouce sur mobile (taille suffisante)

- **UIX-016**: Le contraste DOIT être suffisant pour la lisibilité (WCAG AA minimum)

- **UIX-017**: Tous les champs DOIVENT avoir des labels descriptifs explicites

- **UIX-018**: Les états d'erreur DOIVENT être visuellement distincts (couleur + icône)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Les utilisateurs peuvent compléter le formulaire multi-pages en moins de 5 minutes (premier usage, utilisateur familier avec codes BAAC)

- **SC-002**: 95% des utilisateurs naviguent entre les 6 pages sans confusion grâce aux indicateurs de progression

- **SC-003**: 100% des champs affichent le format "code — libellé" conformément au référentiel

- **SC-004**: Aucune soumission invalide n'atteint l'API (validation complète côté interface)

- **SC-005**: L'interface répond aux soumissions en moins de 5 secondes dans 95% des cas (incluant le temps de l'appel API)

- **SC-006**: 90% des utilisateurs comprennent le résultat de prédiction (probabilité + classe + seuil) sans aide supplémentaire

- **SC-007**: Les utilisateurs non-experts peuvent utiliser l'interface sans formation grâce à l'aide contextuelle par champ

- **SC-008**: L'interface fonctionne correctement sur les navigateurs modernes (Chrome, Firefox, Safari, Edge) sur tablettes et desktops

- **SC-009**: Les menus déroulants sont utilisables confortablement au pouce sur écrans mobiles (tactile responsive)

## Assumptions

1. **API Backend Disponible**: On suppose qu'une API de prédiction (FastAPI) existe et expose un endpoint `/predict` conforme au dictionnaire de données

2. **Format de Réponse API**: On suppose que l'API retourne un objet JSON avec au minimum `{"prediction": "grave|non_grave", "probability": 0.0-1.0}`

3. **Référentiel JSON**: Un fichier JSON centralisé contenant tous les codes BAAC et libellés est disponible ou peut être généré depuis `data_dictionary_catboost_product15.md`

4. **Session State Streamlit**: Streamlit supporte le session state pour préserver les sélections entre les pages (fonctionnalité native depuis Streamlit 0.84.0+)

5. **Pas de Persistance**: Les données non soumises ne sont pas persistées - comportement attendu pour une interface publique sans authentification

6. **Langue**: L'interface est en français, ciblant principalement des utilisateurs francophones

7. **Audience**: Les utilisateurs principaux sont des analystes de sécurité routière, experts, et potentiellement grand public intéressé par la sécurité routière

8. **Volumétrie**: Usage prévu pour des prédictions individuelles (pas de batch), avec un nombre modéré d'utilisateurs simultanés (<100)

9. **Environnement d'Exécution**: L'interface Streamlit sera déployée et accessible via navigateur web

10. **Données Sensibles**: Les données saisies ne sont pas des données personnelles identifiables (pas de RGPD stricte) - uniquement des caractéristiques d'accidents

## Out of Scope

- **Sauvegarde Automatique**: Pas de sauvegarde automatique des saisies en cours - l'utilisateur doit compléter le formulaire en une session

- **Batch Predictions**: La saisie ou l'upload de fichiers CSV pour prédire plusieurs accidents simultanément n'est pas incluse

- **Historique des Prédictions**: Le stockage et l'affichage de l'historique des prédictions passées par utilisateur n'est pas inclus

- **Authentification Utilisateur**: Pas de système de connexion ou de comptes utilisateur - l'interface est publique/anonyme

- **Comparaison de Scénarios**: Pas de fonction pour comparer côte-à-côte plusieurs prédictions (pourrait être ajouté en P4)

- **Visualisations Avancées**: Pas de graphiques d'analyse ou de tableaux de bord d'agrégation - uniquement la prédiction unitaire

- **Export de Résultats**: Pas de fonction d'export PDF/CSV des résultats de prédiction

- **Multi-langue**: Uniquement français - pas de support anglais ou autre langue

- **Optimisation Mobile Native**: Optimisation pour desktop/tablette prioritaire - mobile utilisable mais pas optimal

- **Explainability Avancée**: Pas de SHAP values ou d'explication détaillée de pourquoi le modèle a fait cette prédiction (pourrait être P4 future)

- **Édition Inline du Récap**: Sur la page 6 récap, pas d'édition inline - l'utilisateur doit utiliser "Précédent" pour modifier
