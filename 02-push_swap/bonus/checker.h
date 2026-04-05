/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   checker.h                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/07 00:10:30 by Tsellak           #+#    #+#             */
/*   Updated: 2026/01/07 10:44:12 by Tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef CHECKER_H
# define CHECKER_H

# include <limits.h>
# include <stdlib.h>
# include <unistd.h>

typedef struct s_stack
{
	int				value;
	int				index;
	struct s_stack	*next;
}					t_stack;
// utils
long				ft_atol(const char *nptr);
int					ft_isdigit(int c);
t_stack				*ft_lstlast(t_stack *lst);
char				**ft_split(char const *s, char c);
size_t				ft_strlen(const char *s);
char				*ft_substr(char const *s, unsigned int start, size_t len);
// stack init
void				free_stack(t_stack **stack);
void				stack_init(t_stack **a, char **argv);
int					is_sorted(t_stack *stack);
// parsing utils
int					is_number(char *str);
int					has_duplicates(t_stack *a, int n);
int					ft_strcmp(const char *s1, const char *s2);
void				error_exit(t_stack **a, char **split_str);
void				free_matrix(char **argv);
// swap
void				sa(t_stack **stack_a);
void				sb(t_stack **stack_b);
void				ss(t_stack **stack_a, t_stack **stack_b);
// rotate
void				ra(t_stack **stack_a);
void				rb(t_stack **stack_b);
void				rr(t_stack **stack_a, t_stack **stack_b);
// reverse rotate
void				rra(t_stack **stack_a);
void				rrb(t_stack **stack_b);
void				rrr(t_stack **stack_a, t_stack **stack_b);
// push
void				pa(t_stack **a, t_stack **b);
void				pb(t_stack **b, t_stack **a);

#endif
