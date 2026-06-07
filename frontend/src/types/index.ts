export type WordCategory = 
  | 'standard' 
  | 'archaic' 
  | 'abbreviation' 
  | 'slang' 
  | 'proper_noun' 
  | 'invalid';

export type SolveMode = 
  | 'strict' 
  | 'dictionary' 
  | 'scrabble' 
  | 'crossword' 
  | 'permissive';

export interface MatchResult {
  word: string;
  length: number;
  type: 'full_anagram' | 'sub_anagram';
  confidence: number;
  category: WordCategory;
  zipf_score: number;
}

export interface SolveResponse {
  input: string;
  execution_ms: number;
  total_matches: number;
  full_anagram_count: number;
  sub_anagram_count: number;
  longest_word: string | null;
  matches: MatchResult[];
  mode: SolveMode;
  filtered_count: number;
}

export interface ModeInfo {
  mode: SolveMode;
  description: string;
  min_confidence: number;
  include_abbreviations: boolean;
  include_archaic: boolean;
}

export type SortOption = 'confidence_desc' | 'length_desc' | 'length_asc' | 'alphabetical';

export type FilterOption = 'all' | 'full_anagram' | 'sub_anagram';

export interface HistoryEntry {
  letters: string;
  total_matches: number;
  timestamp: number;
  mode?: SolveMode;
}
