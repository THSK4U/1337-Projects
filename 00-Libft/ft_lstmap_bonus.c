/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstmap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/30 07:59:41 by tsellak           #+#    #+#             */
/*   Updated: 2025/11/01 17:58:44 by tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

t_list	*ft_lstmap(t_list *lst, void *(*f)(void *), void (*del)(void *))
{
	t_list	*cpy_list;
	t_list	*current;
	void	*new;
	t_list	*node;

	if (!lst || !f || !del)
		return (NULL);
	cpy_list = NULL;
	current = lst;
	while (current)
	{
		new = f(current->content);
		node = ft_lstnew(new);
		if (!node)
		{
			del(new);
			ft_lstclear(&cpy_list, del);
			return (NULL);
		}
		ft_lstadd_back(&cpy_list, node);
		current = current->next;
	}
	return (cpy_list);
}
